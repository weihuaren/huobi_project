import logging
import json
from huobi.constant import *
from .client import MyAccountClient
from huobi.client.market import MarketClient
from huobi.utils import *
from .info import volume, volume_average
client = MyAccountClient()
market_client = MarketClient()
def run():
    print("5v  :" + str(volume(CandlestickInterval.MIN5)))
    print("5vj :" + str(volume_average(CandlestickInterval.MIN5)))
    # print("15v :" + str(volume(CandlestickInterval.MIN15)))
    # print("15vj:" + str(volume_average(CandlestickInterval.MIN15)))
    # print("30v :" + str(volume(CandlestickInterval.MIN30)))
    # print("30vj:" + str(volume_average(CandlestickInterval.MIN30)))

                

