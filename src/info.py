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

def volume(interval):
    candlesticks = market_client.get_candlestick(symbol, interval, 1)
    return candlesticks[0].amount

def volume_average(interval):
    candlesticks = market_client.get_candlestick(symbol, interval)
    sum = 0
    for candlestick in candlesticks:
        sum = sum + candlestick.amount
    return sum/len(candlesticks)
                

