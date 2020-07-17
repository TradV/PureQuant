# -*- coding:utf-8 -*-

"""
交易模块

Author: eternal ranger
Date:   2020/07/09
email: interstella.ranger2020@gmail.com
"""
from purequant.exchange.okex import spot_api as okexspot
from purequant.exchange.okex import futures_api as okexfutures
from purequant.exchange.okex import swap_api as okexswap
from purequant.exchange.huobi import huobi_futures as huobifutures
from purequant.utils.time_tools import ts_to_datetime_str, utctime_str_to_ts

class OkexFutures:
    """okex交割合约操作  https://www.okex.com/docs/zh/#futures-README"""
    def __init__(self, access_key, secret_key, passphrase, instrument_id):
        self.access_key = access_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.instrument_id = instrument_id
        self.okex_futures = okexfutures.FutureAPI(self.access_key, self.secret_key, self.passphrase, self.instrument_id)

    def buy(self, price, size, order_type):
        receipt = self.okex_futures.buy(self.instrument_id, price, size, order_type)
        return receipt

    def sell(self, price, size, order_type):
        receipt = self.okex_futures.sell(self.instrument_id, price, size, order_type)
        return receipt

    def sellshort(self, price, size, order_type):
        receipt = self.okex_futures.sellshort(self.instrument_id, price, size, order_type)
        return receipt

    def buytocover(self, price, size, order_type):
        receipt = self.okex_futures.buytocover(self.instrument_id, price, size, order_type)
        return receipt

    def BUY(self, cover_short_price, cover_short_size, open_long_price, open_long_size, order_type):
        receipt = self.okex_futures.BUY(self.instrument_id, cover_short_price, cover_short_size, open_long_price, open_long_size, order_type)
        return receipt

    def SELL(self, cover_long_price, cover_long_size, open_short_price, open_short_size, order_type):
        receipt = self.okex_futures.SELL(self.instrument_id, cover_long_price, cover_long_size, open_short_price, open_short_size, order_type)
        return receipt

    def get_order_list(self, state, limit):
        receipt = self.okex_futures.get_order_list(self.instrument_id, state=state, limit=limit)
        return receipt

    def revoke_order(self, order_id):
        receipt = self.okex_futures.revoke_order(self.instrument_id, order_id)
        if receipt['error_code'] == "0":
            return '撤单成功'
        else:
            return '撤单失败' + receipt['error_message']

    def get_order_info(self, order_id):
        receipt = self.okex_futures.get_order_info(self.instrument_id, order_id)
        return receipt

    def get_kline(self, time_frame):
        if time_frame == "1m" or time_frame == "1M":
            granularity = '60'
        elif time_frame == '3m' or time_frame == "3M":
            granularity = '180'
        elif time_frame == '5m' or time_frame == "5M":
            granularity = '300'
        elif time_frame == '15m' or time_frame == "15M":
            granularity = '900'
        elif time_frame == '30m' or time_frame == "30M":
            granularity = '1800'
        elif time_frame == '1h' or time_frame == "1H":
            granularity = '3600'
        elif time_frame == '2h' or time_frame == "2H":
            granularity = '7200'
        elif time_frame == '4h' or time_frame == "4H":
            granularity = '14400'
        elif time_frame == '6h' or time_frame == "6H":
            granularity = '21600'
        elif time_frame == '12h' or time_frame == "12H":
            granularity = '43200'
        elif time_frame == '1d' or time_frame == "1D":
            granularity = '86400'
        else:
            return 'k线周期错误，只支持【1min 3min 5min 15min 30min 1hour 2hour 4hour 6hour 12hour 1day】'
        receipt = self.okex_futures.get_kline(self.instrument_id, granularity=granularity)
        return receipt

    def get_position(self):
        receipt = self.okex_futures.get_specific_position(instrument_id=self.instrument_id)
        return receipt

    def get_ticker(self):
        receipt = self.okex_futures.get_specific_ticker(instrument_id=self.instrument_id)
        return receipt

    def get_contract_value(self):
        receipt = self.okex_futures.get_products()
        t = 0
        result = {}
        for item in receipt:
            result[item['instrument_id']] = item['contract_val']
            t += 1
        return result

class OkexSpot:
    """okex现货操作  https://www.okex.com/docs/zh/#spot-README"""
    def __init__(self, access_key, secret_key, passphrase, instrument_id):
        self.access_key = access_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.instrument_id = instrument_id
        self.okex_spot = okexspot.SpotAPI(self.access_key, self.secret_key, self.passphrase)

    def buy(self, type, price, size, order_type, notional=""):
        receipt = self.okex_spot.take_order(instrument_id=self.instrument_id, side="buy", type=type, size=size, price=price, order_type=order_type, notional=notional)
        order_id = int(receipt['order_id'])
        if receipt['result'] == False:
            return '交易提醒：' + self.instrument_id + '买入开多失败' + receipt['error_message']
        else:
            order_info = self.okex_spot.get_order_info(self.instrument_id, order_id=order_id)
            if order_info['state'] == '2':
                return "交易提醒：【{}】订单【买入开多】完全成交！成交均价【{}】 数量【{}】 成交金额【{}】".format(self.instrument_id, order_info['price_avg'], order_info['filled_size'], round(float(order_info['filled_size']) * float(order_info['price_avg']), 2))
            else:
                return "交易提醒：【{}】订单【买入开多】失败！".format(self.instrument_id)

    def sell(self, type, price, size, order_type):
        receipt = self.okex_spot.take_order(instrument_id=self.instrument_id, side="sell", type=type, size=size, price=price, order_type=order_type)
        order_id = int(receipt['order_id'])
        if receipt['result'] == False:
            return '交易提醒：' + self.instrument_id + '卖出平多失败' + receipt['error_message']
        else:
            order_info = self.okex_spot.get_order_info(self.instrument_id, order_id=order_id)
            if order_info['state'] == '2':
                return "交易提醒：【{}】订单【卖出平多】完全成交！成交均价【{}】 数量【{}】 成交金额【{}】".format(self.instrument_id, order_info['price_avg'], order_info['filled_size'], round(float(order_info['filled_size']) * float(order_info['price_avg']), 2))
            else:
                return "交易提醒：【{}】订单【卖出平多】失败！".format(self.instrument_id)

    def get_order_list(self, state, limit):
        receipt = self.okex_spot.get_orders_list(self.instrument_id, state=state, limit=limit)
        return receipt

    def revoke_order(self, order_id):
        receipt = self.okex_spot.revoke_order(self.instrument_id, order_id)
        if receipt['error_code'] == "0":
            return '撤单成功'
        else:
            return '撤单失败' + receipt['error_message']

    def get_order_info(self, order_id):
        receipt = self.okex_spot.get_order_info(self.instrument_id, order_id)
        return receipt

    def get_kline(self, time_frame):
        if time_frame == "1m" or time_frame == "1M":
            granularity = '60'
        elif time_frame == '3m' or time_frame == "3M":
            granularity = '180'
        elif time_frame == '5m' or time_frame == "5M":
            granularity = '300'
        elif time_frame == '15m' or time_frame == "15M":
            granularity = '900'
        elif time_frame == '30m' or time_frame == "30M":
            granularity = '1800'
        elif time_frame == '1h' or time_frame == "1H":
            granularity = '3600'
        elif time_frame == '2h' or time_frame == "2H":
            granularity = '7200'
        elif time_frame == '4h' or time_frame == "4H":
            granularity = '14400'
        elif time_frame == '6h' or time_frame == "6H":
            granularity = '21600'
        elif time_frame == '12h' or time_frame == "12H":
            granularity = '43200'
        elif time_frame == '1d' or time_frame == "1D":
            granularity = '86400'
        else:
            return 'k线周期错误，只支持【1min 3min 5min 15min 30min 1hour 2hour 4hour 6hour 12hour 1day】'
        receipt = self.okex_spot.get_kline(self.instrument_id, granularity=granularity)
        return receipt

    def get_position(self):
        receipt = self.okex_spot.get_position(self.instrument_id)
        return receipt


class OkexSwap:
    """okex永续合约操作 https://www.okex.com/docs/zh/#swap-README"""
    def __init__(self, access_key, secret_key, passphrase, instrument_id):
        self.access_key = access_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.instrument_id = instrument_id
        self.okex_swap = okexswap.SwapAPI(self.access_key, self.secret_key, self.passphrase)

    def buy(self, price, size, order_type):
        receipt = self.okex_swap.take_order(instrument_id=self.instrument_id, price=price, size=size, order_type=order_type, type=1)
        if receipt['error_code'] != "0":
            return '交易提醒：' + self.instrument_id + '买入开多失败' + receipt['error_message']
        else:
            order_id = receipt['order_id']
            order_info = self.okex_swap.get_order_info(self.instrument_id, order_id=order_id)
            if order_info['state'] == '2':
                return "交易提醒：【{}】订单【买入开多】完全成交！成交均价【{}】 数量【{}】 成交金额【{}】".format(self.instrument_id, order_info['price_avg'],
                                                                        order_info['filled_qty'], round(
                        int(order_info['contract_val']) * int(order_info['filled_qty']) * float(order_info['price_avg']), 2))
            else:
                return "交易提醒：【{}】订单【买入开多 】失败！".format(self.instrument_id)


    def sell(self, price, size, order_type):
        receipt = self.okex_swap.take_order(instrument_id=self.instrument_id, price=price, size=size, order_type=order_type,
                                            type=3)
        if receipt['error_code'] != "0":
            return '交易提醒：' + self.instrument_id + '卖出平多失败' + receipt['error_message']
        else:
            order_id = receipt['order_id']
            order_info = self.okex_swap.get_order_info(self.instrument_id, order_id=order_id)
            if order_info['state'] == '2':
                return "交易提醒：【{}】订单【卖出平多】完全成交！成交均价【{}】 数量【{}】 成交金额【{}】".format(self.instrument_id, order_info['price_avg'],
                                                                          order_info['filled_qty'], round(
                        int(order_info['contract_val']) * int(order_info['filled_qty']) * float(
                            order_info['price_avg']), 2))
            else:
                return "交易提醒：【{}】订单【卖出平多】失败！".format(self.instrument_id)

    def sellshort(self, price, size, order_type):
        receipt = self.okex_swap.take_order(instrument_id=self.instrument_id, price=price, size=size, order_type=order_type,
                                            type=2)
        if receipt['error_code'] != "0":
            return '交易提醒：' + self.instrument_id + '卖出开空失败' + receipt['error_message']
        else:
            order_id = receipt['order_id']
            order_info = self.okex_swap.get_order_info(self.instrument_id, order_id=order_id)
            if order_info['state'] == '2':
                return "交易提醒：【{}】订单【卖出开空】完全成交！成交均价【{}】 数量【{}】 成交金额【{}】".format(self.instrument_id, order_info['price_avg'],
                                                                          order_info['filled_qty'], round(
                        int(order_info['contract_val']) * int(order_info['filled_qty']) * float(
                            order_info['price_avg']), 2))
            else:
                return "交易提醒：【{}】订单【卖出开空】失败！".format(self.instrument_id)

    def buytocover(self, price, size, order_type):
        receipt = self.okex_swap.take_order(instrument_id=self.instrument_id, price=price, size=size, order_type=order_type,
                                            type=4)
        if receipt['error_code'] != "0":
            return '交易提醒：' + self.instrument_id + '买入平空失败' + receipt['error_message']
        else:
            order_id = receipt['order_id']
            order_info = self.okex_swap.get_order_info(self.instrument_id, order_id=order_id)
            if order_info['state'] == '2':
                return "交易提醒：【{}】订单【买入平空】完全成交！成交均价【{}】 数量【{}】 成交金额【{}】".format(self.instrument_id, order_info['price_avg'],
                                                                          order_info['filled_qty'], round(
                        int(order_info['contract_val']) * int(order_info['filled_qty']) * float(
                            order_info['price_avg']), 2))
            else:
                return "交易提醒：【{}】订单【买入平空】失败！".format(self.instrument_id)

    def BUY(self, cover_short_price, cover_short_size, open_long_price, open_long_size, order_type):
        receipt1 = self.buytocover(cover_short_price, cover_short_size, order_type)
        receipt2 = self.buy(open_long_price, open_long_size, order_type)
        return receipt1 + receipt2


    def SELL(self, cover_long_price, cover_long_size, open_short_price, open_short_size, order_type):
        receipt1 = self.sell(cover_long_price, cover_long_size, order_type)
        receipt2 = self.sellshort(open_short_price, open_short_size, order_type)
        return receipt1 + receipt2

    def get_order_list(self, state, limit):
        receipt = self.okex_swap.get_order_list(self.instrument_id, state=state, limit=limit)
        return receipt

    def revoke_order(self, order_id):
        receipt = self.okex_swap.revoke_order(self.instrument_id, order_id)
        if receipt['error_code'] == "0":
            return '撤单成功'
        else:
            return '撤单失败' + receipt['error_message']

    def get_order_info(self, order_id):
        receipt = self.okex_swap.get_order_info(self.instrument_id, order_id)
        return receipt

    def get_kline(self, time_frame):
        if time_frame == "1m" or time_frame == "1M":
            granularity = '60'
        elif time_frame == '3m' or time_frame == "3M":
            granularity = '180'
        elif time_frame == '5m' or time_frame == "5M":
            granularity = '300'
        elif time_frame == '15m' or time_frame == "15M":
            granularity = '900'
        elif time_frame == '30m' or time_frame == "30M":
            granularity = '1800'
        elif time_frame == '1h' or time_frame == "1H":
            granularity = '3600'
        elif time_frame == '2h' or time_frame == "2H":
            granularity = '7200'
        elif time_frame == '4h' or time_frame == "4H":
            granularity = '14400'
        elif time_frame == '6h' or time_frame == "6H":
            granularity = '21600'
        elif time_frame == '12h' or time_frame == "12H":
            granularity = '43200'
        elif time_frame == '1d' or time_frame == "1D":
            granularity = '86400'
        else:
            return 'k线周期错误，只支持【1min 3min 5min 15min 30min 1hour 2hour 4hour 6hour 12hour 1day】'
        receipt = self.okex_swap.get_kline(self.instrument_id, granularity=granularity)
        return receipt

    def get_position(self):
        receipt = self.okex_swap.get_specific_position(self.instrument_id)
        direction = receipt['holding'][0]['side']
        amount = int(receipt['holding'][0]['position'])
        price = float(receipt['holding'][0]['avg_cost'])
        if amount == 0:
            direction = None
        result = {'direction': direction, 'amount': amount, 'price': price}
        return result

    def get_contract_value(self):
        receipt = self.okex_swap.get_instruments()
        t = 0
        result = {}
        for item in receipt:
            result[item['instrument_id']]=item['contract_val']
            t += 1
        return result

class HuobiFutures:
    """火币合约 https://huobiapi.github.io/docs/dm/v1/cn/#5ea2e0cde2"""
    def __init__(self, access_key, secret_key, instrument_id):
        self.access_key = access_key
        self.secret_key = secret_key
        self.instrument_id = instrument_id
        self.huobi_futures = huobifutures.HuobiFutures(self.access_key, self.secret_key)

    def buy(self, price, size, order_type):
        """
        火币交割合约下单买入开多，只支持季度和次季合约，只支持20倍杠杆
        :param self.instrument_id: 合约ID 例如：'BTC-201225'
        :param price:   下单价格
        :param size:    下单数量
        :param order_type:  0：限价单
                            1：只做Maker（Post only）
                            2：全部成交或立即取消（FOK）
                            3：立即成交并取消剩余（IOC）
                            4：对手价下单
        :return:
        """
        symbol = self.instrument_id[0:3]
        if self.instrument_id[6:8] == '03' or self.instrument_id[6:8] == '09':
            contract_type = "quarter"
        elif self.instrument_id[6:8] == '06' or self.instrument_id[6:8] == '12':
            contract_type = "next_quarter"
        else:
            return "交易提醒：合约ID错误，只可输入当季或者次季合约ID，请重新输入！"
        contract_code = self.instrument_id[0:3] + self.instrument_id[4:10]
        order_price_type = 0
        if order_type == 0:
            order_price_type = 'limit'
        elif order_type == 1:
            order_price_type = "post_only"
        elif order_type == 2:
            order_price_type = "fok"
        elif order_type == 3:
            order_price_type = "ioc"
        elif order_type == 4:
            order_price_type = "opponent"
        self.huobi_futures.send_contract_order(symbol=symbol, contract_type=contract_type, contract_code=contract_code,
                        client_order_id='', price=price, volume=size, direction='buy',
                        offset='open', lever_rate=20, order_price_type=order_price_type)

    def get_kline(self, time_frame):
        if self.instrument_id[6:8] == '03' or self.instrument_id[6:8] == '09':
            symbol = "BTC_CQ"
        elif self.instrument_id[6:8] == '06' or self.instrument_id[6:8] == '12':
            symbol = "BTC_NQ"
        else:
            return "交易提醒：合约ID错误，只可输入当季或者次季合约ID，请重新输入！"
        if time_frame == '1m' or time_frame == '1M':
            period = '1min'
        elif time_frame == '5m' or time_frame == '5M':
            period = '5min'
        elif time_frame == '15m' or time_frame == '15M':
            period = '15min'
        elif time_frame == '30m' or time_frame == '30M':
            period = '30min'
        elif time_frame == '1h' or time_frame == '1H':
            period = '60min'
        elif time_frame == '4h' or time_frame == '4H':
            period = '4hour'
        elif time_frame == '1d' or time_frame == '1D':
            period = '1day'
        else:
            return "k线周期错误，k线周期只能是【1m, 5m, 15m, 30m, 1h, 4h, 1d】之一"
        records = self.huobi_futures.get_contract_kline(symbol=symbol, period=period)['data']
        length = len(records)

        j = 1
        list = []
        while j < length:
            for item in records:
                item = [ts_to_datetime_str(item['id']), item['open'], item['high'], item['low'], item['close'], item['vol'], round(item['amount'], 2)]
                list.append(item)
                j+=1
        list.reverse()
        return list

