from .util import get_logger
import json
import time
from huobi.constant import *
from .client import MyAccountClient
from huobi.client.market import MarketClient
from huobi.utils import *
from .indicators import get_indicators

logger = get_logger('algorithm')

client = MyAccountClient()
market_client = MarketClient()

def run():
    m1 = None
    d1 = None
    k1 = None
    k2 = None
    logger.info(f"程序开始运行")
    while True:
        time.sleep(0.5)
        cs_min1 = get_indicators(CandlestickInterval.MIN1)
        print(cs_min1)
        if (not k2) and (not m1) and (not d1) and (not k1) \
        and (cs_min1['m'] < 0) \
        and (cs_min1['d'] < 0):
            m1 = cs_min1['m']
            d1 = cs_min1['d']
            k1 = cs_min1['k']

        if (not k2) and m1 and d1 and k1 \
        and cs_min1['d'] > 0:
            m1 = None
            d1 = None
            k1 = None
            continue

        if m1 and d1 and k1:
            m1 = min(m1, cs_min1['m'])
            d1 = min(d1, cs_min1['d'])
            k1 = min(k1, cs_min1['k'])

        if (not k2) and m1 and d1 and k1 \
        and (d1 < m1) \
        and cs_min1['m'] > m1 \
        and cs_min1['d'] > d1 \
        and cs_min1['d'] < cs_min1['m'] \
        and cs_min1['k'] < k1 \
        and cs_min1['v'] > 2.9*cs_min1['average_v']:
            k2 = cs_min1['k']
            buyin_price = market_client.get_market_trade(symbol="btcusdt")[0].price
            logger.info(f"发现买点")
            logger.info(f"买点: {buyin_price}")
            logger.info(f"买点参考数据")
            logger.info(f"k1={k1} k2={cs_min1['k']}")
            logger.info(f"m1={m1} m2={cs_min1['m']}")
            logger.info(f"d1={d1} d2={cs_min1['d']}")

        if k2 \
        and (cs_min1['d'] > 0 \
        or cs_min1['d'] < d1 \
        or cs_min1['k'] < 0.9*k2):
            k2 = cs_min1['k']
            buyin_price = market_client.get_market_trade(symbol="btcusdt")[0].price
            logger.info(f"发现卖点")
            logger.info(f"卖点: {buyin_price}")
            logger.info(f"卖点参考数据")
            logger.info(f"k1={k1} k2= {k2} k3={cs_min1['k']}")
            logger.info(f"m1={m1} m2={cs_min1['m']}")
            logger.info(f"d1={d1} d2={cs_min1['d']}")
            break



        
        

                               








                        





    
    
                

