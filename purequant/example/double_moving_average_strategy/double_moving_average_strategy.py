from purequant.indicators import Indicators
from purequant.trade import OkexFutures
from purequant.position import Position
from purequant.market import Market
from purequant.utils.push import dingtalk
from purequant.storage import storage
from purequant.utils.time_tools import get_localtime
from purequant.config import config
from purequant.utils.logger import Logger

class Strategy:

    def __init__(self, instrument_id, time_frame, fast_length, slow_length, long_stop, short_stop):
        """双均线策略"""

        print("{}程序开始运行！".format(get_localtime()))
        config.loads('config.json')  # 载入配置文件

        # 在第一次运行程序时，将总资金数据保存至数据库中
        start_asset = 20
        storage.save_asset_and_profit('trade', 'asset', get_localtime(), 0, start_asset)

        # 读取数据库中保存的总资金数据
        self.total_asset = storage.read_mysql_datas(0, 'trade', 'asset', 'asset', '>')[-1][-1]

        self.counter = 0  # 计数器
        self.long_stop = long_stop   # 多单止损幅度
        self.short_stop = short_stop    # 空单止损幅度
        self.access_key = config.access_key     # 读取配置文件中保存的api信息
        self.secret_key = config.secret_key
        self.passphrase = config.passphrase

        self.instrument_id = instrument_id      # 合约ID
        self.time_frame = time_frame        # k线周期
        self.fast_length = fast_length   # 短周期均线长度
        self.slow_length = slow_length  # 长周期均线长度
        self.exchange = OkexFutures(self.access_key, self.secret_key, self.passphrase, self.instrument_id) # 初始化交易所
        self.position = Position(self.exchange, self.instrument_id, self.time_frame) # 初始化potion
        self.market = Market(self.exchange, self.instrument_id, self.time_frame)    # 初始化market
        self.logger = Logger("config.json") # 初始化logger
        self.indicators = Indicators(self.exchange, self.instrument_id, self.time_frame)

    def begin_trade(self):
        try:
            # 计算策略信号
            fast_ma = self.indicators.MA(self.fast_length)
            slow_ma = self.indicators.MA(self.slow_length)
            cross_over = fast_ma[-2] >= slow_ma[-2] and fast_ma[-3] < slow_ma[-3]
            cross_below = slow_ma[-2] >= fast_ma[-2] and slow_ma[-3] < fast_ma[-3]
            if self.indicators.BarUpdate():
                self.counter = 0

            if self.counter < 1:
                # 按照策略信号开平仓
                if cross_over: # 金叉时
                    if self.position.amount() == 0:
                        info = self.exchange.buy(None, round(self.total_asset/self.market.last()/self.market.contract_value()), 4)
                        dingtalk(info)
                    if self.position.direction() == 'short':
                        profit = self.position.short_profit()
                        self.total_asset += profit
                        storage.save_asset_and_profit('trade', 'asset', get_localtime(), profit, self.total_asset)
                        info = self.exchange.BUY(None, self.position.amount(), None, round(self.total_asset/self.market.last()/self.market.contract_value()), 4)
                        dingtalk(info)
                if cross_below: # 死叉时
                    if self.position.amount() == 0:
                        info = self.exchange.sellshort(None, round(self.total_asset/self.market.last()/self.market.contract_value()), 4)
                        dingtalk(info)
                    if self.position.direction() == 'long':
                        profit = self.position.long_profit()
                        self.total_asset += profit
                        storage.save_asset_and_profit('trade', 'asset', get_localtime(), profit, self.total_asset)
                        info = self.exchange.SELL(None, self.position.amount(), None, round(self.total_asset/self.market.last()/self.market.contract_value()), 4)
                        dingtalk(info)
                # 止损
                if self.position.amount() > 0:
                    if self.position.direction() == 'long' and self.market.last() <= self.position.price() * self.long_stop:
                        profit = self.position.long_profit()
                        self.total_asset += profit
                        storage.save_asset_and_profit('trade', 'asset', get_localtime(), profit, self.total_asset)
                        info = self.exchange.sell(None, self.position.amount(), 4)
                        dingtalk(info)
                        self.counter += 1
                    if self.position.direction() == 'short' and self.market.last() >= self.position.price() * self.short_stop:
                        profit = self.position.short_profit()
                        self.total_asset += profit
                        storage.save_asset_and_profit('trade', 'asset', get_localtime(), profit, self.total_asset)
                        info = self.exchange.buytocover(None, self.position.amount(), 4)
                        dingtalk(info)
                        self.counter += 1
        except Exception as msg:
                self.logger.error(msg)

if __name__ == "__main__":
    strategy = Strategy("TRX-USDT-201225", "1m", 10, 20, 0.95, 1.05)
    while True:
        strategy.begin_trade()