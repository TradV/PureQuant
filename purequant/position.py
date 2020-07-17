# -*- coding:utf-8 -*-

"""
持仓信息模块

Author: eternal ranger
Date:   2020/07/09
email: interstella.ranger2020@gmail.com
"""
from purequant.market import Market

class Position:

    def __init__(self, platform, instrument_id, time_frame):
        self.platform = platform
        self.instrument_id = instrument_id
        self.time_frame = time_frame
        self.market = Market(self.platform, self.instrument_id, self.time_frame)
        self.contract_value = self.market.contract_value()

    def direction(self):
        """获取当前持仓方向"""
        result = self.platform.get_position()['direction']
        return result

    def amount(self):
        """获取当前持仓数量"""
        result = self.platform.get_position()['amount']
        return result

    def price(self):
        """获取当前的持仓价格"""
        result = self.platform.get_position()['price']
        return result

    def long_profit(self):
        """计算平多的单笔交易利润"""
        result = (self.market.last() - self.price()) * (self.amount() * self.contract_value)
        return result

    def short_profit(self):
        """计算平空的单笔交易利润"""
        result = (self.price() - self.market.last()) * (self.amount() * self.contract_value)
        return result