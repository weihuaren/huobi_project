import logging
import json
from huobi.constant import *
from .client import MyAccountClient
from huobi.client.market import MarketClient
from huobi.utils import *
from .indicators import get_indicators
from pprint import pprint
client = MyAccountClient()
market_client = MarketClient()

def run():
    indicators_min5 = get_indicators(CandlestickInterval.MIN5)
    indicators_min15 = get_indicators(CandlestickInterval.MIN15)
    indicators_min30 = get_indicators(CandlestickInterval.MIN30)
    indicators_min60 = get_indicators(CandlestickInterval.MIN60)

    pprint(indicators_min15)
    pprint(indicators_min15)
                

