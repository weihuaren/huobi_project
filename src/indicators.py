import logging
import json
from functools import reduce
from huobi.constant import *
from huobi.client.market import MarketClient
from huobi.utils import *
from .client import MyAccountClient
import pandas as pd

client = MyAccountClient()
market_client = MarketClient()
symbol = "btcusdt"

def get_indicators(interval):
    candlesticks = market_client.get_candlestick(symbol, interval)
    macd =  _get_macd(candlesticks)
    average = _close_volume_average(candlesticks[:20])
    average_ma10 = _close_volume_average(candlesticks[:10])
    return {
        "volume": candlesticks[0].amount,
        "average_volume": average['average_volume'],
        "average_close": average['average_close'],
        "average_close_ma10": average_ma10['average_close'],
        "dif": macd['dif'],
        "histogram": macd['histogram'],
        "dea": macd['dea'],
        "previous_histogram": macd['previous_histogram'],
        "close":  candlesticks[0].close
    }
def _close_volume_average(candlesticks):
    volume = 0
    close = 0
    for candlestick in candlesticks:
        volume = volume + candlestick.amount
        close = close + candlestick.close
    return {
        'average_volume': volume/len(candlesticks),
        'average_close': close/len(candlesticks)
    }

def _get_macd(candlesticks):
    market_data = []
    for stick in candlesticks:
        market_data.append({'close': stick.close})
    market_data.reverse()
    df = pd.DataFrame.from_dict(market_data)
    df['ema12'] = pd.Series.ewm(df['close'], span=12).mean()
    df['ema26'] = pd.Series.ewm(df['close'], span=26).mean()
    df['dif']= df['ema12'] - df['ema26']
    df['dea']= pd.Series.ewm(df['dif'], span=9).mean()
    df['histogram']= df['dif'] - df['dea']
    return {
        'dif': df['dif'].iloc[-1],
        'histogram': df['histogram'].iloc[-1],
        'dea': df['dea'].iloc[-1],
        'previous_histogram': df['histogram'].iloc[-2],
    }


