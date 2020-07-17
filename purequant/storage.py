# -*- coding:utf-8 -*-

"""
数据存储与读取

Author: eternal ranger
Date:   2020/07/09
email: interstella.ranger2020@gmail.com
"""
import logging, mysql.connector
from purequant.utils import time_tools
from purequant.indicators import Indicators

class Strorage:
    """K线等各种数据的存储与读取"""

    def __init__(self):
        self.old_kline = 0

    def save_asset_and_profit(self, database, data_sheet, timestamp, profit, asset):
        """存储单笔交易盈亏与总资金信息至mysql数据库"""
        conn = mysql.connector.connect(user='root', password='root', database=database)
        cursor = conn.cursor()
        cursor.execute(
            'insert into {} (timestamp, profit, asset) values (%s, %s, %s)'.format(
                data_sheet),
            [timestamp, profit, asset])
        conn.commit()
        cursor.close()
        conn.close()

    def save_kline_func(self, database, data_sheet, timestamp, open, high, low, close, volume, currency_volume):
        """此函数专为k线存储的函数使用"""
        # 连接数据库
        conn = mysql.connector.connect(user='root', password='root', database=database)
        # 打开游标
        cursor = conn.cursor()
        # 插入数据
        cursor.execute(
            'insert into {} (timestamp, open, high, low, close, volume, currency_volume) values (%s, %s, %s, %s, %s, %s, %s)'.format(
                data_sheet),
            [timestamp, open, high, low, close, volume, currency_volume])
        # 提交事务
        conn.commit()
        # 关闭游标和连接
        cursor.close()
        conn.close()

    def kline_save(self, platform, database, data_sheet, instrument_id, time_frame):
        """
        从交易所获取k线数据，并将其存储至数据库中
        :param platform: 交易所
        :param database: 数据库名称
        :param data_sheet: 数据表名称
        :param instrument_id: 要获取k线数据的交易对名称或合约ID
        :param time_frame: k线周期，如'60'为一分钟，'86400'为一天，字符串格式
        :return: "获取的历史数据已存储至mysql数据库！"
        """
        result = platform.get_kline(instrument_id, time_frame)
        result.reverse()
        for data in result:
            self.save_kline_func(database, data_sheet, data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        return "获取的历史数据已存储至mysql数据库！"

    def kline_storage(self, platform, database, data_sheet, instrument_id, time_frame):
        """
        实时获取上一根k线存储至数据库中。
        :param database: 数据库名称
        :param data_sheet: 数据表名称
        :param instrument_id: 交易对或合约id
        :param time_frame: k线周期，如'60'为一分钟，'86400'为一天，字符串格式
        :return:
        """
        indicators = Indicators(platform, instrument_id, time_frame)
        if indicators.BarUpdate() == True:
            last_kline = platform.get_kline(instrument_id, time_frame)[1]
            if last_kline != self.old_kline:    # 若获取得k线不同于已保存的上一个k线
                timestamp = last_kline[0]
                open = last_kline[1]
                high = last_kline[2]
                low = last_kline[3]
                close = last_kline[4]
                volume = last_kline[5]
                currency_volume = last_kline[6]
                self.save_kline_func(database, data_sheet, timestamp, open, high, low, close, volume, currency_volume)
                # print(last_kline)
                self.old_kline = last_kline  # 将刚保存的k线设为旧k线
            else:
                return

    def read_mysql_datas(self, data, database, datasheet, field, operator):  # 获取数据库满足条件的数据
        """
        查询数据库中满足条件的数据
        :param data: 要查询的数据，数据类型由要查询的数据决定
        :param database: 数据库名称
        :param datasheet: 数据表名称
        :param field: 字段
        :return: 返回值查询到的数据，如未查询到则返回None
        """
        # 连接数据库
        conn = mysql.connector.connect(user='root', password='root', database=database, buffered = True)
        # 打开游标
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM {} WHERE {} {} '{}'".format(datasheet, field, operator, data))
        LogData = cursor.fetchall()  # 取出了数据库数据
        # 关闭游标和连接
        cursor.close()
        conn.close()
        return LogData

    def read_mysql_specific_data(self, data, database, datasheet, field):  # 获取数据库满足条件的数据
        """
        查询数据库中满足条件的数据
        :param data: 要查询的数据，数据类型由要查询的数据决定
        :param database: 数据库名称
        :param datasheet: 数据表名称
        :param field: 字段
        :return: 返回值查询到的数据，如未查询到则返回None
        """
        # 连接数据库
        conn = mysql.connector.connect(user='root', password='root', database=database, buffered = True)
        # 打开游标
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(datasheet, field, data))
        LogData = cursor.fetchone()  # 取出了数据库数据
        # 关闭游标和连接
        cursor.close()
        conn.close()
        return LogData

    def text_save(self, content, filename, mode='a'):
        """
        保存数据至txt文件。
        :param content: 要保存的内容,必须为string格式
        :param filename:文件路径及名称
        :param mode:
        :return:
        """
        file = open(filename, mode)
        file.write(content + '\n')
        file.close()

    def text_read(self, filename):
        """
        读取txt文件中的数据。
        :param filename: 文件路径、文件名称。
        :return:返回一个包含所有文件内容的列表，其中元素均为string格式
        """
        try:
            file = open(filename, 'r')
        except IOError:
            error = '打开txt文件失败，请检查文件！'
            return error
        content = file.readlines()
        for i in range(len(content)):
            content[i] = content[i][:len(content[i]) - 1]
            file.close()
        return content



storage = Strorage()
