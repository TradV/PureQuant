import numpy as np
import talib
from purequant.utils import time_tools

class Indicators:

    def __init__(self, platform, instrument_id, time_frame):
        self.platform = platform
        self.instrument_id = instrument_id
        self.time_frame = time_frame
        self.last_time_stamp = 0

    def ATR(self, length):
        """指数移动平均线"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        high_array = np.zeros(kline_length)
        low_array = np.zeros(kline_length)
        close_array = np.zeros(kline_length)
        t1 = 0
        t2 = 0
        t3 = 0
        for item in records:
            high_array[t1] = item[2]
            low_array[t2] = item[3]
            close_array[t3] = item[4]
            t1 += 1
            t2 += 1
            t3 += 1
        result = (talib.ATR(high_array, low_array, close_array, timeperiod=length))
        return result

    def BOLL(self, length):
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.BBANDS(close_array, timeperiod=length, nbdevup=2, nbdevdn=2, matype=0))
        upperband = result[0]
        middleband = result[1]
        lowerband = result[2]
        dict = {"upperband": upperband, "middleband": middleband, "lowerband": lowerband}
        return dict

    def BarUpdate(self):
        """
        K线更新
        :param self.platform: 交易所对象
        :param self.instrument_id: 合约id
        :param self.time_frame: k线周期
        :return: 若k线更新，返回True；否则返回False
        """
        records = self.platform.get_kline(self.time_frame)
        kline_length = len(records)
        current_timestamp = time_tools.utctime_str_to_ts(records[kline_length - 1][0])
        if current_timestamp != self.last_time_stamp:  # 如果当前时间戳不等于lastTime，说明k线更新
            if current_timestamp < self.last_time_stamp:
                return
            else:
                self.last_time_stamp = current_timestamp
                return True
        else:
            return False

    def CurrentBar(self):
        """获取k线数据的长度"""
        records = self.platform.get_kline(self.time_frame)
        kline_length = len(records)
        return kline_length

    def HIGHEST(self, length):
        """周期最高价"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        high_array = np.zeros(kline_length)
        t = 0
        for item in records:
            high_array[t] = item[2]
            t += 1
        result = (talib.MAX(high_array, length))
        return result

    def MA(self, length):
        """
        移动平均线(简单移动平均)
        :param self.platform: 交易所对象
        :param self.instrument_id: 标的名称
        :param self.time_frame: k线周期
        :param length: 均线长度
        :return: 返回值为一个包含各个bar上周期均价的列表
        """
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t+=1
        result = (talib.SMA(close_array, length))
        return result

    def MACD(self, fastperiod, slowperiod, signalperiod):
        """
        计算MACD
        :param self.platform: 交易所
        :param self.instrument_id: 合约ID
        :param self.time_frame: k线周期
        :return: 返回一个字典 {'DIF': DIF数组, 'DEA': DEA数组, 'MACD': MACD数组}
        """
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.MACD(close_array, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod))
        DIF = result[0]
        DEA = result[1]
        MACD = result[2] * 2
        dict = {'DIF': DIF, 'DEA': DEA, 'MACD': MACD}
        return dict

    def EMA(self, length):
        """指数移动平均线"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.EMA(close_array, length))
        return result

    def KAMA(self, length):
        """适应性移动平均线"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.KAMA(close_array, length))
        return result

    def KDJ(self, fastk_period, slowk_period, slowd_period):
        """
        计算k值和d值
        :param self.platform:
        :param self.instrument_id:
        :param self.time_frame:
        :return: 返回一个字典，{'k': k值数组， 'd': d值数组}
        """
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        high_array = np.zeros(kline_length)
        low_array = np.zeros(kline_length)
        close_array = np.zeros(kline_length)
        t1 = 0
        t2 = 0
        t3 = 0
        for item in records:
            high_array[t1] = item[2]
            low_array[t2] = item[3]
            close_array[t3] = item[4]
            t1 += 1
            t2 += 1
            t3 += 1

        result = (talib.STOCH(high_array, low_array, close_array, fastk_period=fastk_period,
                                                                slowk_period=slowk_period,
                                                                slowk_matype=0,
                                                                slowd_period=slowd_period,
                                                                slowd_matype=0))
        slowk = result[0]
        slowd = result[1]
        dict = {'k': slowk, 'd': slowd}
        return dict

    def LOWEST(self, length):
        """周期最低价"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        low_array = np.zeros(kline_length)
        t = 0
        for item in records:
            low_array[t] = item[3]
            t += 1
        result = (talib.MIN(low_array, length))
        return result

    def OBV(self):
        """OBV"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.OBV(close_array, self.VOLUME()))
        return result

    def RSI(self, length):
        """RSI"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.RSI(close_array, timeperiod=length))
        return result

    def ROC(self, length):
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.ROC(close_array, timeperiod=length))
        return result

    def STOCHRSI(self, timeperiod, fastk_period, fastd_period):
        """
        计算STOCHRSI
        :param self.platform: 交易所
        :param self.instrument_id: 合约ID
        :param self.time_frame: k线周期
        :return: 返回一个字典  {'STOCHRSI': STOCHRSI数组, 'fastk': fastk数组}
        """
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.STOCHRSI(close_array, timeperiod=timeperiod, fastk_period=fastk_period, fastd_period=fastd_period, fastd_matype=0))
        STOCHRSI = result[1]
        fastk = talib.MA(STOCHRSI, 3)
        dict = {'stochrsi': STOCHRSI, 'fastk': fastk}
        return dict

    def SAR(self):
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        high_array = np.zeros(kline_length)
        low_array = np.zeros(kline_length)
        t1 = 0
        t2 = 0
        for item in records:
            high_array[t1] = item[2]
            low_array[t2] = item[3]
            t1 += 1
            t2 += 1
        result = (talib.SAR(high_array, low_array, acceleration=0.02, maximum=0.2))
        return result

    def STDDEV(self, length):
        """标准偏差"""
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.STDDEV(close_array, timeperiod=length, nbdev=1))
        return result


    def TRIX(self, length):
        records = self.platform.get_kline(self.time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.TRIX(close_array, timeperiod=length))
        return result

    def VOLUME(self):
        """成交量"""
        records = self.platform.get_kline(self.time_frame)
        length = len(records)
        records.reverse()
        t = 0
        volume_array = np.zeros(length)
        for item in records:
            volume_array[t] = item[5]
            t += 1
        return volume_array




