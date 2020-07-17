from .client import Client
from .consts import *


class FutureAPI(Client):

    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False, first=False):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, first)

    # query position
    def get_position(self):
        return self._request_without_params(GET, FUTURE_POSITION)

    # query specific position
    def get_specific_position(self, instrument_id):
        result = self._request_without_params(GET, FUTURE_SPECIFIC_POSITION + str(instrument_id) + '/position')
        if int(result['holding'][0]['long_qty']) > 0:
            dict = {'direction': 'long', 'amount': int(result['holding'][0]['long_qty']), 'price': float(result['holding'][0]['long_avg_cost'])}
            return dict
        elif int(result['holding'][0]['short_qty']) > 0:
            dict = {'direction': 'short', 'amount': int(result['holding'][0]['short_qty']), 'price': float(result['holding'][0]['short_avg_cost'])}
            return dict
        else:
            dict = {'direction': 'none', 'amount': 0, 'price': 0.0}
            return dict

    # query accounts info
    def get_accounts(self):
        return self._request_without_params(GET, FUTURE_ACCOUNTS)

    # query coin account info
    def get_coin_account(self, underlying):
        return self._request_without_params(GET, FUTURE_COIN_ACCOUNT + str(underlying))

    # query leverage
    def get_leverage(self, underlying):
        return self._request_without_params(GET, FUTURE_GET_LEVERAGE + str(underlying) + '/leverage')

    # set leverage
    def set_leverage(self, underlying, leverage, instrument_id='', direction=''):
        params = {'leverage': leverage}
        if instrument_id:
            params['instrument_id'] = instrument_id
        if direction:
            params['direction'] = direction
        return self._request_with_params(POST, FUTURE_SET_LEVERAGE + str(underlying) + '/leverage', params)

    # query ledger
    def get_ledger(self, underlying, after='', before='', limit='', type=''):
        params = {}
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        if type:
            params['type'] = type
        return self._request_with_params(GET, FUTURE_LEDGER + str(underlying) + '/ledger', params, cursor=True)

    # take order
    def take_order(self, instrument_id, type, price, size, client_oid='', order_type='0', match_price='0'):
        """
        交割合约下单。
        所有参数类型：	String
        :param instrument_id: 合约ID  e.g. 'BTC-USDT-201225'
        :param type:1:开多 2:开空 3:平多 4:平空 参数填数字
        :param price:委托价格
        :param size:买入或卖出合约的数量（以张计数）
        :param client_oid:由您设置的订单ID来识别您的订单,格式是字母（区分大小写）+数字 或者 纯字母（区分大小写），1-32位字符 （不能重复）
        :param order_type:0：普通委托（order type不填或填0都是普通委托）
                          1：只做Maker（Post only） 2：全部成交或立即取消（FOK）
                          3：立即成交并取消剩余（IOC）
                          4：市价委托
        :param match_price:是否以对手价下单(0:不是; 1:是)，默认为0，当取值为1时，price字段无效。当以对手价下单，order_type只能选择0（普通委托）
        :return:
        """
        if type == "buy" or type == "BUY":
            type = 1
        elif type == "sellshort" or type == "SELLSHORT":
            type = 2
        elif type == "sell" or type == "SELL":
            type = 3
        elif type == "buytocover" or type == "BUYTOCOVER":
            type = 4
        else:
            print("type error, please correct...")
        params = {'client_oid': client_oid, 'instrument_id': instrument_id, 'type': type, 'order_type': order_type, 'price': price, 'size': size, 'match_price': match_price}
        return self._request_with_params(POST, FUTURE_ORDER, params)

    def buy(self, instrument_id, price, size, order_type):
        result = self.take_order(instrument_id, 'buy', price, size, order_type=order_type)
        order_info = self.get_order_info(instrument_id, order_id=result['order_id'])
        return '交易提醒' + order_info

    def sell(self, instrument_id, price, size, order_type):
        result = self.take_order(instrument_id, 'sell', price, size, order_type=order_type)
        order_info = self.get_order_info(instrument_id, order_id=result['order_id'])
        return '交易提醒' + order_info

    def sellshort(self, instrument_id, price, size, order_type):
        result = self.take_order(instrument_id, 'sellshort', price, size, order_type=order_type)
        order_info = self.get_order_info(instrument_id, order_id=result['order_id'])
        return '交易提醒' + order_info

    def buytocover(self, instrument_id, price, size, order_type):
        result = self.take_order(instrument_id, 'buytocover', price, size, order_type=order_type)
        order_info = self.get_order_info(instrument_id, order_id=result['order_id'])
        return '交易提醒' + order_info

    def BUY(self, instrument_id, short_price, short_size, long_price, long_size, order_type):
        result1 = self.take_order(instrument_id, 'buytocover', short_price, short_size, order_type=order_type)
        result2 = self.take_order(instrument_id, 'buy', long_price, long_size, order_type=order_type)
        order_info1 = self.get_order_info(instrument_id, order_id=result1['order_id'])
        order_info2 = self.get_order_info(instrument_id, order_id=result2['order_id'])
        return '交易提醒' + order_info1 + order_info2

    def SELL(self, instrument_id, long_price, long_size, short_price, short_size, order_type):
        result1 = self.take_order(instrument_id, 'sell', long_price, long_size, order_type=order_type)
        result2 = self.take_order(instrument_id, 'sellshort', short_price, short_size, order_type=order_type)
        order_info1 = self.get_order_info(instrument_id, order_id=result1['order_id'])
        order_info2 = self.get_order_info(instrument_id, order_id=result2['order_id'])
        return '交易提醒' + order_info1 + order_info2

    # take orders
    def take_orders(self, instrument_id, orders_data):
        params = {'instrument_id': instrument_id, 'orders_data': orders_data}
        return self._request_with_params(POST, FUTURE_ORDERS, params)

    # revoke order
    def revoke_order(self, instrument_id, order_id='', client_oid=''):
        if order_id:
            return self._request_without_params(POST, FUTURE_REVOKE_ORDER + str(instrument_id) + '/' + str(order_id))
        elif client_oid:
            return self._request_without_params(POST, FUTURE_REVOKE_ORDER + str(instrument_id) + '/' + str(client_oid))

    # revoke orders

    def revoke_orders(self, instrument_id, order_ids='', client_oids=''):
        params = {}
        if order_ids:
            params = {'order_ids': order_ids}
        elif client_oids:
            params = {'client_oids': client_oids}
        return self._request_with_params(POST, FUTURE_REVOKE_ORDERS + str(instrument_id), params)

    # query order list
    def get_order_list(self, instrument_id, state, after='', before='', limit=''):
        params = {'state': state}
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, FUTURE_ORDERS_LIST + str(instrument_id), params, cursor=True)

    # query order info
    def get_order_info(self, instrument_id, order_id='', client_oid=''):
        if order_id:
            result = self._request_without_params(GET, FUTURE_ORDER_INFO + str(instrument_id) + '/' + str(order_id))
            instrument_id = result['instrument_id']
            action = None
            if result['type'] == '1':
                action = "买入开多"
            elif result['type'] == '2':
                action = "卖出开空"
            if result['type'] == '3':
                action = "卖出平多"
            if result['type'] == '4':
                action = "买入平空"
            # 开仓时
            if (action == "买入开多" or action == "卖出开空"):
                if int(result['state']) == 2:
                    return "【{}】订单【{}】完全成交！成交均价【{}】 数量【{}】 成交金额【{}】".format(instrument_id, action, result['price_avg'], result['filled_qty'], round(int(result['contract_val']) * int(result['filled_qty']) * float(result['price_avg']), 2))
                else:
                    return "【{}】订单【{}】失败！".format(instrument_id, action)
            # 平仓时
            if (action == "卖出平多" or action == "买入平空"):
                if int(result['state']) == 2:
                    return "【{}】订单【{}】完全成交！成交均价【{}】 数量【{}】 成交金额【{}】 收益【{}】".format(instrument_id, action, result['price_avg'], result['filled_qty'], round(int(result['contract_val']) * int(result['filled_qty']) * float(result['price_avg']), 2), result['pnl'])
                else:
                    return "【{}】订单【{}】失败！".format(instrument_id, action)
        elif client_oid:
            return self._request_without_params(GET, FUTURE_ORDER_INFO + str(instrument_id) + '/' + str(client_oid))

    # query fills
    def get_fills(self, instrument_id, order_id='', after='', before='', limit=''):
        params = {'instrument_id': instrument_id}
        if order_id:
            params['order_id'] = order_id
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, FUTURE_FILLS, params, cursor=True)

    # set margin_mode
    def set_margin_mode(self, underlying, margin_mode):
        params = {'underlying': underlying, 'margin_mode': margin_mode}
        return self._request_with_params(POST, FUTURE_MARGIN_MODE, params)

    # close_position
    def close_position(self, instrument_id, direction):
        params = {'instrument_id': instrument_id, 'direction': direction}
        return self._request_with_params(POST, FUTURE_CLOSE_POSITION, params)

    # cancel_all
    def cancel_all(self, instrument_id, direction):
        params = {'instrument_id': instrument_id, 'direction': direction}
        return self._request_with_params(POST, FUTURE_CANCEL_ALL, params)

    # take order_algo
    def take_order_algo(self, instrument_id, type, order_type, size, trigger_price='', algo_price='', algo_type='', callback_rate='', algo_variance='', avg_amount='', price_limit='', sweep_range='', sweep_ratio='', single_limit='', time_interval=''):
        params = {'instrument_id': instrument_id, 'type': type, 'order_type': order_type, 'size': size}
        if order_type == '1': # 止盈止损参数（最多同时存在10单）
            params['trigger_price'] = trigger_price
            params['algo_price'] = algo_price
            if algo_type:
                params['algo_type'] = algo_type
        elif order_type == '2': # 跟踪委托参数（最多同时存在10单）
            params['callback_rate'] = callback_rate
            params['trigger_price'] = trigger_price
        elif order_type == '3': # 冰山委托参数（最多同时存在6单）
            params['algo_variance'] = algo_variance
            params['avg_amount'] = avg_amount
            params['price_limit'] = price_limit
        elif order_type == '4': # 时间加权参数（最多同时存在6单）
            params['sweep_range'] = sweep_range
            params['sweep_ratio'] = sweep_ratio
            params['single_limit'] = single_limit
            params['price_limit'] = price_limit
            params['time_interval'] = time_interval
        return self._request_with_params(POST, FUTURE_ORDER_ALGO, params)

    # cancel_algos
    def cancel_algos(self, instrument_id, algo_ids, order_type):
        params = {'instrument_id': instrument_id, 'algo_ids': algo_ids, 'order_type': order_type}
        return self._request_with_params(POST, FUTURE_CANCEL_ALGOS, params)

    # get order_algos
    def get_order_algos(self, instrument_id, order_type, status='', algo_id='', before='', after='', limit=''):
        params = {'order_type': order_type}
        if status:
            params['status'] = status
        elif algo_id:
            params['algo_id'] = algo_id
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, FUTURE_GET_ORDER_ALGOS + str(instrument_id), params)

    def get_trade_fee(self):
        return self._request_without_params(GET, FUTURE_TRADE_FEE)

    # get products info
    def get_products(self):
        return self._request_without_params(GET, FUTURE_PRODUCTS_INFO)

    # get depth
    def get_depth(self, instrument_id, size='', depth=''):
        params = {'size': size, 'depth': depth}
        return self._request_with_params(GET, FUTURE_DEPTH + str(instrument_id) + '/book', params)

    # get ticker
    def get_ticker(self):
        return self._request_without_params(GET, FUTURE_TICKER)

    # get specific ticker
    def get_specific_ticker(self, instrument_id):
        return self._request_without_params(GET, FUTURE_SPECIFIC_TICKER + str(instrument_id) + '/ticker')

    # query trades
    def get_trades(self, instrument_id, after='', before='', limit=''):
        params = {}
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, FUTURE_TRADES + str(instrument_id) + '/trades', params, cursor=True)

    # query k-line
    def get_kline(self, instrument_id, granularity='', start='', end=''):
        params = {'granularity': granularity, 'start': start, 'end': end}
        # 按时间倒叙 即由结束时间到开始时间
        return self._request_with_params(GET, FUTURE_KLINE + str(instrument_id) + '/candles', params)

        # 按时间正序 即由开始时间到结束时间
        # data = self._request_with_params(GET, FUTURE_KLINE + str(instrument_id) + '/candles', params)
        # return list(reversed(data))

    # query index
    def get_index(self, instrument_id):
        return self._request_without_params(GET, FUTURE_INDEX + str(instrument_id) + '/index')

    # query rate
    def get_rate(self):
        return self._request_without_params(GET, FUTURE_RATE)

    # query estimate price
    def get_estimated_price(self, instrument_id):
        return self._request_without_params(GET, FUTURE_ESTIMAT_PRICE + str(instrument_id) + '/estimated_price')

    # query the total platform of the platform
    def get_holds(self, instrument_id):
        return self._request_without_params(GET, FUTURE_HOLDS + str(instrument_id) + '/open_interest')

    # query limit price
    def get_limit(self, instrument_id):
        return self._request_without_params(GET, FUTURE_LIMIT + str(instrument_id) + '/price_limit')

    # query limit price
    def get_liquidation(self, instrument_id, status, limit='', froms='', to=''):
        params = {'status': status}
        if limit:
            params['limit'] = limit
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        return self._request_with_params(GET, FUTURE_LIQUIDATION + str(instrument_id) + '/liquidation', params)

    # query holds amount
    def get_holds_amount(self, instrument_id):
        return self._request_without_params(GET, HOLD_AMOUNT + str(instrument_id) + '/holds')

    # query mark price
    def get_mark_price(self, instrument_id):
        return self._request_without_params(GET, FUTURE_MARK + str(instrument_id) + '/mark_price')

    # set auto margin
    def set_auto_margin(self, underlying, type):
        params = {'underlying': underlying, 'type': type}
        return self._request_with_params(POST, FUTURE_AUTO_MARGIN, params)

    # change margin
    def change_margin(self, instrument_id, direction, type, amount):
        params = {'instrument_id': instrument_id, 'direction': direction, 'type': type, 'amount': amount}
        return self._request_with_params(POST, FUTURE_CHANGE_MARGIN, params)

    # get history settlement
    def get_history_settlement(self, instrument_id, start='', limit='', end=''):
        params = {'instrument_id': instrument_id}
        if start:
            params['start'] = start
        if limit:
            params['limit'] = limit
        if end:
            params['end'] = end
        return self._request_with_params(GET, FUTURE_HISTORY_SETTLEMENT, params)
