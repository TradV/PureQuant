from purequant.storage import storage
from purequant.trade import OkexSwap

apikey = "2d3c69bd-754c-4f88-8929-5fc98ba71a44"
secretkey = "C3B79F99AB78B9F9645AB2F4A5C746E0"
passphrase = '123456'

instrument_id = "BTC-USDT-SWAP"
time_frame = '60'
exchange = OkexSwap(apikey, secretkey, passphrase)

storage.kline_save(exchange, 'records', 'btc', instrument_id, time_frame)