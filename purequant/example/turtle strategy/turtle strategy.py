from purequant.utils.time_tools import get_localtime
from purequant.config import config
from purequant.trade import OkexFutures
from purequant.indicators import Indicators
from purequant.market import Market
from purequant.position import Position
from purequant.utils.logger import Logger
from purequant.utils.push import dingtalk, twilio

class Strategy:
    """海龟交易策略"""

    def __init__(self, instrument_id, time_frame, contract_value):

        print("{} 策略开始运行...".format(get_localtime()))

        config.loads("config.json")
        access_key = config.access_key
        secret_key = config.secret_key
        passphrase = config.passphrase
        self.exchange = OkexFutures(access_key, secret_key, passphrase, self.instrument_id)
        self.instrument_id = instrument_id
        self.time_frame = time_frame
        self.contract_value = contract_value
        self.market = Market(self.exchange, self.instrument_id, self.time_frame)
        self.position = Position(self.exchange, self.instrument_id, self.time_frame)
        self.logger = Logger("config.json")
        self.indicators = Indicators(self.exchange, self.instrument_id, self.time_frame)
        self.ATRLength = 20    # 平均波动周期
        self.boLength = 20  # 短周期 BreakOut Length
        self.fsLength = 55  # 长周期 FailSafe Length
        self.teLength = 10   # 离市周期 Trailing Exit Length
        self.LastProfitableTradeFilter = 1   # 使用入市过滤条件
        self.TotalEquity = 100  # 策略总资产
        self.PreBreakoutFailure = False  # 前一次是否突破失败
        self.CurrentEntries = 0  # 当前持仓的开仓次数
        self.counter = 0

    def begin_trade(self):
        try:
            AvgTR = self.indicators.ATR(self.ATRLength) # 计算真实波幅
            t = 0
            for item in AvgTR[-21:-1]:
                t += item
            PreN = t
            N = (PreN/20) + (AvgTR[-1])
            Units = (self.TotalEquity * 0.01) / (N*self.contract_value) # 计算每一份头寸大小
            self.logger.debug(Units)
            return
            # 计算短周期唐奇安通道
                # 唐奇安通道上轨，延后1个Bar
            DonchianHi = self.indicators.HIGHEST(self.boLength)[-2]
                # 唐奇安通道下轨，延后1个Bar
            DonchianLo = self.indicators.LOWEST(self.boLength)[-2]
            # 计算长周期唐奇安通道
                # 唐奇安通道上轨，延后1个Bar，长周期
            fsDonchianHi = self.indicators.HIGHEST(self.fsLength)[-2]
                # 唐奇安通道下轨，延后1个Bar，长周期
            fsDonchianLo = self.indicators.LOWEST(self.fsLength)[-2]
            # 计算止盈唐奇安通道
                # 离市时判断需要的N周期最低价
            ExitLowestPrice = self.indicators.LOWEST(self.teLength)[-2]
                # 离市时判断需要的N周期最高价
            ExitHighestPrice = self.indicators.HIGHEST(self.teLength)[-2]
            if self.indicators.BarUpdate():
                self.counter = 0
            if self.counter < 1:
                # 当不使用过滤条件，或者使用过滤条件,并且条件PreBreakoutFailure为True时，短周期开仓
                if self.indicators.CurrentBar() >= self.boLength and self.position.amount() == 0 and (self.LastProfitableTradeFilter != 1 or self.PreBreakoutFailure == False):
                    if self.market.high(-1) >= DonchianHi: # 突破了短周期唐奇安通道上轨
                        receipt = self.exchange.buy(None, Units, 4) # 市价开多
                        dingtalk(receipt)
                        self.CurrentEntries += 1
                        self.PreBreakoutFailure = False  # 将标识重置为默认值，根据离场时的盈亏情况再修改
                    if self.market.low(-1) <= DonchianLo: # 突破了短周期唐奇安通道下轨
                        receipt = self.exchange.sellshort(None, Units, 4) # 市价开空
                        dingtalk(receipt)
                        self.CurrentEntries += 1
                        self.PreBreakoutFailure = False # 将标识重置为默认值，根据离场时的盈亏情况再修改
                # 长周期突破开仓，其他逻辑和短周期突破开仓一样
                if (self.indicators.CurrentBar() >= self.fsLength) and (self.position.amount() == 0):
                    if self.market.high(-1) >= fsDonchianHi:
                        receipt = self.exchange.buy(None, Units, 4)
                        dingtalk(receipt)
                        self.CurrentEntries += 1
                        self.PreBreakoutFailure = False
                    if self.market.low(-1) <= fsDonchianLo:
                        receipt = self.exchange.sellshort(None, Units, 4)
                        dingtalk(receipt)
                        self.CurrentEntries += 1
                        self.PreBreakoutFailure = False

                if self.position.direction() == "long": # 持多仓的情况
                    if self.market.low(-1) <= ExitLowestPrice:    # 跌破止盈价
                        receipt = self.exchange.sell(None, self.position.amount(), 4) # 市价平所有多单仓位
                        self.counter += 1
                        dingtalk(receipt)
                    else:
                        # 加仓指令
                        '''以最高价为标准，判断是否能加仓，并限制最大加仓次数
                           如果价格过前次开仓价格1/2N,则直接加仓
                        '''
                        while (self.market.high(-1) >= (self.position.price() + 0.5 * N)) and (self.CurrentEntries < 4):
                            receipt = self.exchange.buy(None, Units, 4)
                            dingtalk(receipt)
                            self.CurrentEntries += 1
                        # 止损指令
                        if (self.market.low(-1) <= (self.position.price() - 2 * N)):   # 如果回落大于最后下单价格-2n，就止损
                            receipt = self.exchange.sell(None, self.position.amount(), 4) # 全部止损平仓
                            self.counter += 1
                            dingtalk(receipt)
                            self.PreBreakoutFailure = True  # 记录为突破失败，下次交易将使用长周期开仓
                elif self.position.direction() == "short": # 持空头的情况，除方向以外，其他逻辑和上面持多仓的一致
                    if self.market.high(-1) >= ExitHighestPrice:
                        receipt = self.exchange.buytocover(None, self.position.amount(), 4)
                        self.counter += 1
                        dingtalk(receipt)
                    else:
                        while (self.market.low(-1) <= (self.position.price() - 0.5 * N)) and (self.CurrentEntries < 4):
                            receipt = self.exchange.sellshort(None, Units, 4)
                            dingtalk(receipt)
                            self.CurrentEntries += 1
                        if (self.market.high(-1) >= (self.position.price() + 2 * N)):
                            receipt = self.exchange.buytocover(None, self.position.amount(), 4)
                            self.counter += 1
                            dingtalk(receipt)
                            self.PreBreakoutFailure = True
        except Exception as msg:
            self.logger.error(msg)

if __name__ == "__main__":
    strategy = Strategy("BTC-USDT-201225", "1m", 0.01)
    # while True:
    #     strategy.begin_trade()

    strategy.begin_trade()


