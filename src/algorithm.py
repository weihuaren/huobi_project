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
    
    k1 = None
    m1 = None
    #if: 5v >= 4*5vj
    indicators_min5 = get_indicators(CandlestickInterval.MIN5)
    pprint(indicators_min5)
    if indicators_min5['volume'] >= 4*indicators_min5['average_volume']:
        #if: 15v >= 4*15vj
        indicators_min15 = get_indicators(CandlestickInterval.MIN15)
        if indicators_min15['volume'] >= 4*indicators_min15['average_volume']:
            #if 5d < 5m
            if indicators_min5['dif'] < indicators_min5['histogram']:
                #if 15d < 15m
                if indicators_min15['dif'] < indicators_min15['histogram']:
                    #if current 30m > previous 30m
                    indicators_min30 = get_indicators(CandlestickInterval.MIN30)
                    if indicators_min30['histogram'] > indicators_min30['previous_histogram']:
                        #if current 60m > previous 60m
                        indicators_min60 = get_indicators(CandlestickInterval.MIN60)
                        # set k1, m1, d1 as the lowest point
                        if indicators_min60['histogram'] > indicators_min60['previous_histogram']:
                            k1 = indicators_min5['close']
                            m1 = indicators_min5['histogram']
                            print("buy k1 +- 0.5%")
                        # if k2 > previous candlestick moving average 20 close
                        if indicators_min5['close'] > indicators_min5['previous_average_close']:
                            print("sell")
                        





    
    
                

