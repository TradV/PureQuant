import sys, traceback
from purequant.utils.time_tools import get_localtime
from purequant.indicators import Indicators
from purequant.trade import OkexFutures
from purequant.config import config
from purequant.position import Position
from purequant.market import Market
from purequant.storage import storage
from purequant.utils.push import dingtalk
from purequant.utils.logger import Logger

class Strategy:
    """价格区间突破多空策略"""

    def __init__(self, instrument_id, time_frame):
        print("{}程序开始运行！".format(get_localtime()))
        config.loads("config.json") # 载入配置文件
        # 在第一次运行程序时，将总资金数据保存至数据库中
        start_asset = 20
        storage.save_asset_and_profit('trade', 'asset', get_localtime(), 0, start_asset)
        # 读取数据库中保存的总资金数据
        self.total_asset = storage.read_mysql_datas(0, 'trade', 'asset', 'asset', '>')[-1][-1]

        self.counter = 0    # 计数器
        self.instrument_id = instrument_id  # 合约ID
        self.time_frame = time_frame  # k线周期
        self.exchange = OkexFutures(config.access_key, config.secret_key, config.passphrase, self.instrument_id) # 交易所
        self.position = Position(self.exchange, self.instrument_id, self.time_frame)  # position
        self.market = Market(self.exchange, self.instrument_id, self.time_frame)  # market
        self.logger = Logger("config.json")     # logger
        self.indicators = Indicators(self.exchange, self.instrument_id, self.time_frame)
        self.Length = 50    # 开仓长度参数
        self.StopLength = 40  # 止损长度参数
        self.IPS = 4  # 保护止损波动率参数
        self.AtrVal = 10   # 波动率参数

    def begin_trade(self):
        try:
            myATR = self.indicators.ATR(self.AtrVal)[-1]   # 平均真实波幅
            Upperband = self.indicators.HIGHEST(self.Length)[-2]  # 做多通道最高价
            Lowerband = self.indicators.LOWEST(self.Length)[-2]  # 做空通道最低价
            LongStop =  self.indicators.LOWEST(self.StopLength)[-2]  # 做多通道止损价
            ShortStop = self.indicators.HIGHEST(self.StopLength)[-2]  # 做空通道止损价
            self.ProtectStopLong = 0
            self.ProtectStopShort = 0
            if self.indicators.BarUpdate():  # 若k线更新，则计数器归零
                self.counter = 0
            if self.counter < 1:
                # 多头系统入场。当前不是多头持仓，并且当根bar的最高价高于做多通道最高价
                if self.indicators.CurrentBar() >= self.Length and self.position.direction() != "long" and self.market.high(-1) >= Upperband:
                    if self.position.amount() == 0:  # 若无持仓，直接开多
                        receipt = self.exchange.buy(None, round(self.total_asset/self.market.last()/self.market.contract_value()), 4)  # 价格大于长周期最高价区间入场做多
                        dingtalk(receipt)  # 钉钉推送下单结果
                        self.ProtectStopLong = self.position.price() - self.IPS * myATR  # 计算初始止损的值
                    else:   # 若持空头，平空开多
                        receipt = self.exchange.BUY(None, self.position.amount(), None, round(self.total_asset/self.market.last()/self.market.contract_value()), 4)
                        dingtalk(receipt)
                        self.ProtectStopLong = self.position.price() - self.IPS * myATR  # 计算初始止损的值
                # 空头系统入场。当前不是空头持仓，并且当根 bar 的最低价低于做空通道最低价
                if self.indicators.CurrentBar() >= self.Length and self.position.direction() != "short" and self.market.low(-1) <= Lowerband:
                    if self.position.amount() == 0:
                        receipt = self.exchange.sellshort(None, round(self.total_asset/self.market.last()/self.market.contract_value()), 4)  # 价格大于长周期最高价区间入场做多
                        dingtalk(receipt)
                        self.ProtectStopShort = self.position.price() + self.IPS * myATR  # 计算初始止损的值
                    else:
                        receipt = self.exchange.SELL(None, self.position.amount(), None, round(self.total_asset/self.market.last()/self.market.contract_value()), 4)
                        dingtalk(receipt)
                        self.ProtectStopShort = self.position.price() + self.IPS * myATR  # 计算初始止损的值

                if self.position.direction() == "long":  # 持多单时，计算多头是否需要平仓
                    # 价格低于入场价以下一定 ATR 幅度止损,价格低于短周期最低价区间也出场,使用两者中更高的价格
                    StopLine = max(self.ProtectStopLong, LongStop)             # 止损线
                    if self.market.last() <= StopLine:
                        profit = self.position.long_profit()
                        self.total_asset += profit
                        storage.save_asset_and_profit('trade', 'asset', get_localtime(), profit, self.total_asset)  # 计算单笔盈亏与总资金，并将数据存入数据库
                        receipt = self.exchange.sell(None, self.position.amount(), 4)
                        dingtalk(receipt)
                        self.counter += 1  # 止损后计数器加1，当根bar不再进行开仓等操作
                if self.position.direction() == "short":  # 持空单时，计算空头是否需要平仓
                    StopLine = min(self.ProtectStopShort, ShortStop)   # 价格高于入场价以上一定 ATR 幅度止损,价格高于短周期最高价区间也出场,使用两者中更低的价格
                    if self.market.last() >= StopLine:  # 如果当前 bar 最高价大于两个止损价中的较高者
                        profit = self.position.short_profit()
                        self.total_asset += profit
                        storage.save_asset_and_profit('trade', 'asset', get_localtime(), profit, self.total_asset)
                        receipt = self.exchange.buytocover(None, self.position.amount(), 4)
                        dingtalk(receipt)
                        self.counter += 1
        except Exception:
            self.logger.error(sys.exc_info()[0:3])
            self.logger.error(traceback.extract_tb(sys.exc_info()[2]))

if __name__ == "__main__":
    strategy = Strategy("TRX-USDT-201225", "1m")
    while True:
        strategy.begin_trade()
