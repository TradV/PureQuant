# -*- coding:utf-8 -*-

"""
市场行情模块

Author: eternal ranger
Date:   2020/07/11
email: interstella.ranger2020@gmail.com
"""

class Market:

    def __init__(self, platform, instrument_id, time_frame):
        self.platform = platform
        self.instrument_id = instrument_id
        self.time_frame = time_frame

    def last(self):
        """获取交易对的最新成交价"""
        result = float(self.platform.get_ticker()['last'])
        return result

    def open(self, param):
        """获取交易对当前k线上的开盘价"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        result = float((records)[param][1])
        return result

    def high(self, param):
        """获取交易对当前k线上的最高价"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        result = float((records)[param][2])
        return result

    def low(self, param):
        """获取交易对当前k线上的最低价"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        result = float((records)[param][3])
        return result

    def close(self, param):
        """获取交易对当前k线上的收盘价"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        result = float((records)[param][4])
        return result

    def contract_value(self):
        """获取合约面值"""
        contract_value = int(self.platform.get_contract_value()['{}'.format(self.instrument_id)])
        return contract_value