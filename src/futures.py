import requests
import json
from auth import post
BASE_URL = 'https://api.hbdm.com'

access_key = ''
access_secret = ''

def get_klines(symbol='BTC_CQ', period='1min', size=200):
    r = requests.get(f'{BASE_URL}/market/history/kline?period={period}&size={size}&symbol={symbol}')
    return r.json()['data']

def trade():
    result = post(access_key, access_secret, 'api.hbdm.com', '/linear-swap-api/v1/swap_cross_order', data={
        "contract_code": "BTC-USDT",
        "direction": "buy",
        "offset":"open",
        "lever_rate":1,
        "volume": 1,
        "order_price_type":"opponent_ioc",
    })
    print(result)

def close():
    result = post(access_key, access_secret, 'api.hbdm.com', '/linear-swap-api/v1/swap_cross_lightning_close_position', data={
        "contract_code": "BTC-USDT",
        "direction": "sell",
        "offset":"close",
        "volume": 1,
    })
    print(result)

def query():
    result = post(access_key, access_secret, 'api.hbdm.com', '/linear-swap-api/v1/swap_cross_position_limit', data={
        "contract_code": "BTC-USDT",
    })
    print(result)

query()


