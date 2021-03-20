import requests
import json
from types import SimpleNamespace

def get_klines(symbol='BTC_CQ', period='1min', size=200):
    r = requests.get(f'https://api.hbdm.com/market/history/kline?period={period}&size={size}&symbol={symbol}')
    return r.json()['data']