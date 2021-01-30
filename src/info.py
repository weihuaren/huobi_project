import logging
import json
from functools import reduce
from huobi.constant import *
from huobi.client.market import MarketClient
from huobi.utils import *
from .client import MyAccountClient

client = MyAccountClient()
market_client = MarketClient()
symbol = "btcusdt"

import pandas as pd

def trade_info(interval, ma_length, fast_length, slow_length, signal_length):
    candlesticks = market_client.get_candlestick(symbol, interval)
    current_close = candlesticks[0].close

    market_data = []
    for stick in candlesticks:
        market_data.append({'close': stick.close})
    print(market_data)
    market_data.reverse()
    df = pd.DataFrame.from_dict(market_data)
    df['ema12'] = pd.Series.ewm(df['close'], span=12).mean()
    df['ema26'] = pd.Series.ewm(df['close'], span=26).mean()
    df['dif']= df['ema12'] - df['ema26']
    df['dea']= pd.Series.ewm(df['dif'], span=9).mean()
    df['histogram']= df['dif'] - df['dea']
    print(df.to_markdown())
    dif = (df['dif'].iloc[-1])
    histogram = (df['histogram'].iloc[-1])
    dea = (df['dea'].iloc[-1])
    result = {
        "volume": candlesticks[0].amount,
        "volume_average": volume_average(candlesticks[:ma_length]),
        "dif": dif,
        "histogram": histogram,
        "dea": dea

    }
    return result

def volume_average(candlesticks):
    sum = 0
    for candlestick in candlesticks:
        sum = sum + candlestick.amount
    return sum/len(candlesticks)

def close_price_average(candlesticks):
    sum = 0
    for candlestick in candlesticks:
        sum = sum + candlestick.close
    return sum/len(candlesticks)


