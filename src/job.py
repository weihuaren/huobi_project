import logging
import json
from huobi.constant import *
from .client import MyAccountClient
from huobi.client.market import MarketClient
from huobi.utils import *
from .info import trade_info
from pprint import pprint
client = MyAccountClient()
market_client = MarketClient()

def run():
    # print(trade_info(CandlestickInterval.MIN5, 20))
    pprint(trade_info(CandlestickInterval.MIN5, ma_length=20, fast_length=12, slow_length=26, signal_length=9))

                

