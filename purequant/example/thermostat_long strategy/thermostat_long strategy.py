from purequant.market import Market
from purequant.utils.time_tools import get_localtime
from purequant.trade import OkexFutures
from purequant.config import config
from purequant.indicators import Indicators
from purequant.position import Position


class Strategy:
    """恒温器做多策略"""

    def __init__(self, instrument_id, time_frame):
        print("{} 策略开始运行...".format(get_localtime()))
        config.loads('config.json')

        self.instrument_id = instrument_id
        self.time_frame = time_frame
        self.exchange = OkexFutures(config.access_key, config.secret_key, config.passphrase, self.instrument_id)

        self.market = Market(self.exchange, self.instrument_id, self.time_frame)
        self.indicators = Indicators(self.exchange, self.instrument_id, self.time_frame)
        self.position = Position(self.exchange, self.instrument_id, self.time_frame)

        self.atrLength = 10  # 真实波幅参数
        self.swingPrcnt1 = 0.50  # 震荡市开仓参数
        self.swingPrcnt2 = 0.75  # 震荡市开仓参数
        self.bollingerLengths = 30  # 布林通道参数
        self.numStdDevs = 2  # 布林通道参数
        self.swingTrendSwitch = 20  # 潮汐指数小于此值为震荡市，否则为趋势市

    def begin_trade(self):
        # 计算潮汐指数用以区分震荡市与趋势市
        cmiVal = abs(self.market.close(-2) - self.market.close(-31)) / (self.indicators.HIGHEST(32) - self.indicators.LOWEST(32)) * 100
        trendLokBuy = (self.market.low(-2) + self.market.low(-3) + self.market.low(-4)) / 3
        trendLokSell = (self.market.high(-2) + self.market.high(-3) + self.market.high(-4)) / 3
        # 关键价格
        keyOfDay = (self.market.high(-2) + self.market.low(-2) + self.market.close(-2)) / 3
        # 震荡市中收盘价大于关键价格为宜卖市，否则为宜买市
        buyEasierDay = False  # 宜买市
        sellEasierDay = False   # 宜卖市
        sellEasierDay = True if (self.market.close(-2) > keyOfDay) else False
        buyEasierDay = True if (self.market.close(-2) <= keyOfDay) else False
        # 计算震荡市的进场价格
        myATR = self.indicators.ATR(self.atrLength)
        if buyEasierDay == True:
            self.swingBuyPt = self.market.open(-1) + self.swingPrcnt1*myATR[-2]
            self.swingSellPt = self.market.open(-1) - self.swingPrcnt2*myATR[-2]
        if sellEasierDay == True:
            swingBuyPt = self.market.open(-1) + self.swingPrcnt2 * myATR[-2]
            swingSellPt = self.market.open(-1) - self.swingPrcnt1 * myATR[-2]
        swingBuyPt = max(self.swingBuyPt, trendLokBuy)
        swingSellPt = min(self.swingSellPt, trendLokSell)
        # 计算趋势市的进场价格
        MidLine = self.indicators.MA(self.bollingerLengths)
        Band = self.indicators.STDDEV(self.bollingerLengths)
        upBand = MidLine + self.numStdDevs*Band
        dnBand = MidLine - self.numStdDevs*Band
        trendBuyPt = upBand   # 趋势市的买触发价格
        trendSellPt = dnBand  # 趋势市的卖触发价格

        # 震荡市
        if self.indicators.CurrentBar() >= 30 and cmiVal < self.swingTrendSwitch:
            if self.position.direction() != "long" and self.market.high(-1) >= swingBuyPt:
                self.exchange.buy()



if __name__ == "__main__":
    strategy = Strategy("TRX-USDT-201225", '1d')
    # strategy.begin_trade()
    print(strategy.position.contract_value)