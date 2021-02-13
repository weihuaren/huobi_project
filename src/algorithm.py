import logging
import json
import time
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
    d1 = None  
    d1_15 = None  
    k2 = None
    k3 = None
    
    while not k1:
        time.sleep(5)
        indicators_min5 = get_indicators(CandlestickInterval.MIN5)
        indicators_min15 = get_indicators(CandlestickInterval.MIN15)
        indicators_min60 = get_indicators(CandlestickInterval.MIN60)
        indicators_min240 = get_indicators(CandlestickInterval.HOUR4)
        # if: 5v >= 4*5vj
        if indicators_min5['volume'] >= 4*indicators_min5['average_volume']:
            # if: 15v >= 4*15vj
            if indicators_min15['volume'] >= 4*indicators_min15['average_volume']:
                # if 5d < 5m
                if indicators_min5['dif'] < indicators_min5['histogram']:
                    # if 15d < 15m
                    if indicators_min15['dif'] < indicators_min15['histogram']:
                        # if current 30m > previous 30m
                        if indicators_min60['histogram'] > indicators_min60['previous_histogram']:
                            # if current 60m > previous 60m
                            if indicators_min240['histogram'] > indicators_min240['previous_histogram']:
                                k1 = indicators_min5['close']
                                m1 = indicators_min5['histogram']
                                m1_15 = indicators_min15['histogram']
                                d1 = indicators_min5['dif']
                                d1_15 = indicators_min15['dif']
                                print("buy USD -> BTC")
    
    while not k2:
        time.sleep(5)
        indicators_min5 = get_indicators(CandlestickInterval.MIN5)
        # if:k2=80%5j20 (+- 0.5%)
        if 0.8*indicators_min5['average_close']*0.995 <= indicators_min5['close'] <= 0.8*indicators_min5['average_close']*1.005:
            k2 = indicators_min5['close']
            print("sell")
    
    while not k3:
        time.sleep(5)
        indicators_min5 = get_indicators(CandlestickInterval.MIN5)
        indicators_min15 = get_indicators(CandlestickInterval.MIN15)
        indicators_min60 = get_indicators(CandlestickInterval.MIN60)
        indicators_min240 = get_indicators(CandlestickInterval.HOUR4)
        # if:5v>=2*5v均
        if indicators_min5['volume'] >= 2*indicators_min5['average_volume']:
            # if：15v>=90%15v均
            indicators_min15['volume'] >= 0.9*indicators_min15['average_volume']:
                # if: k3 = 0.8*k1 (+- 0.5%)   
                if  0.8*k1*0.995 <= indicators_min5['close'] <= 0.8*k1*1.005:
                    # if:5-d>5-d1
                    if indicators_min5['dif'] > d1:
                        # if：15-d1<15-d
                        if indicators_min15['dif'] > d1_15:
                            #  if：5-m>5-m1                            
                            if indicators_min5['histogram'] > m1:
                                # If：15-m1<15m
                                if indicators_min15['histogram'] > m1_15:
                                    # If:当下k线60m>前一根k线60m
                                    if indicators_min60['histogram'] > indicators_min60['previous_histogram']:
                                        # If:当下k线240m>前一根k线240m
                                        if indicators_min240['histogram'] > indicators_min240['previous_histogram']:
                                            k3 = indicators_min5['close']
                                            print('buy')

    k4 = None
    m4 = None
    d4 = None
    while True:
        time.sleep(5)
        indicators_min5 = get_indicators(CandlestickInterval.MIN5)
        if not K4 or indicators_min5['close'] < 0:
            K4 = indicators_min5['close']
            m4 = indicators_min5['histogram']
            d4 = indicators_min5['dif']
        else if k4 and k4 < 0 and indicators_min5['close'] > 0:
            K4 = indicators_min5['close']
            m4 = indicators_min5['histogram']
            d4 = indicators_min5['dif']
        else if k4 and k4 > 0 and indicators_min5['close'] > 0:
            if indicators_min5['close'] > k4:
                K4 = indicators_min5['close']
                m4 = indicators_min5['histogram']
                d4 = indicators_min5['dif']
                
            else:

            K4 = indicators_min5['close']
            m4 = indicators_min5['histogram']
            d4 = indicators_min5['dif']
        

                               








                        





    
    
                

