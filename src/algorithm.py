from .util import get_logger
import json
import time
from huobi.constant import *
from .client import MyAccountClient
from huobi.client.market import MarketClient
from huobi.utils import *
from .indicators import get_indicators
from pprint import pprint


logger = get_logger('algorithm')

client = MyAccountClient()
market_client = MarketClient()

def run_long():
    m1 = None
    d1 = None
    k1 = None
    k1_min = None
    k2 = None
    logger.info(f"上升策略程序开始运行")
    while True:
        time.sleep(1)
        try :
            data = get_indicators()
            if data == 'error':
                continue
            if (not k2) and (not m1) and (not d1) and (not k1) \
            and (data['m'] < 0) \
            and (data['d'] < 0):
                m1 = data['m']
                d1 = data['d']
                k1 = data['k']
                k1_min = data['k']
                continue

            if (not k2) and m1 and d1 and k1 \
            and data['d'] > 0:
                m1 = None
                d1 = None
                k1 = None
                k1_min = None
                continue

            if m1 and d1 and k1:
                m1 = min(m1, data['m'])
                k1_min = min(k1_min, data['k'])
                if data['d'] < d1:
                    d1 =  data['d']
                    k1 = k1_min

            if (not k2) and m1 and d1 and k1 \
            and (d1 < m1) \
            and data['m'] > m1 \
            and data['d'] > d1 \
            and data['d'] < data['m'] \
            and data['k'] < k1:
            # and data['v'] > 2.9*data['average_v']:
                k2 = data['k']
                buyin_price = market_client.get_market_trade(symbol="btcusdt")[0].price
                logger.info(f"上升发现买点")
                logger.info(f"上升买点: {buyin_price}")
                logger.info(f"上升买点参考数据")
                logger.info(f"k1={k1} k2={data['k']}")
                logger.info(f"m1={m1} m2={data['m']}")
                logger.info(f"d1={d1} d2={data['d']}")

            if k2 and data['k'] < k2*0.994:
                logger.info(f"上升止损平仓")
                logger.info(f"上升止损平仓k: {data['k']}")
                break
            if k2 \
            and (data['d'] > 0 \
            or data['d'] < d1 \
            or data['k'] < 0.9*k2):
                k2 = data['k']
                buyin_price = market_client.get_market_trade(symbol="btcusdt")[0].price
                logger.info(f"上升发现卖点")
                logger.info(f"上升卖点: {buyin_price}")
                logger.info(f"上升卖点参考数据")
                logger.info(f"k1={k1} k2= {k2} k3={data['k']}")
                logger.info(f"m1={m1} m2={data['m']}")
                logger.info(f"d1={d1} d2={data['d']}")
                break
        except Exception as e:
            logger.error(e)
            break

def run_short():
    m1 = None
    d1 = None
    k1 = None
    k2 = None
    logger.info(f"下降策略程序开始运行")
    while True:
        time.sleep(1)
        try :
            logger.info(f'short m1:{m1} d1:{d1} k1:{k1} k2:{k2}')
            data = get_indicators()
            if data == 'error':
                continue

            if (not k2) and (not m1) and (not d1) and (not k1) \
            and (data['m'] > 0) \
            and (data['d'] > 0):
                m1 = data['m']
                d1 = data['d']
                k1 = data['k']
                continue
            if (not k2) and m1 and d1 and k1 \
            and data['d'] < 0:
                m1 = None
                d1 = None
                k1 = None
                continue

            if m1 and d1 and k1:
                m1 = min(m1, data['m'])
                d1 = min(d1, data['d'])
                k1 = min(k1, data['k'])

            if (not k2) and m1 and d1 and k1 \
            and (d1 > m1) \
            and data['m'] < m1 \
            and data['d'] < d1 \
            and data['d'] > data['m'] \
            and data['k'] > k1:
            # and data['v'] < 2.9*data['average_v']:
                k2 = data['k']
                buyin_price = market_client.get_market_trade(symbol="btcusdt")[0].price
                logger.info(f"下降发现买点")
                logger.info(f"下降买点: {buyin_price}")
                logger.info(f"下降买点参考数据")
                logger.info(f"k1={k1} k2={data['k']}")
                logger.info(f"m1={m1} m2={data['m']}")
                logger.info(f"d1={d1} d2={data['d']}")

            if k2 \
            and (data['d'] < 0 \
            or data['d'] > d1 \
            or data['k'] > 0.9*k2):
                k2 = data['k']
                buyin_price = market_client.get_market_trade(symbol="btcusdt")[0].price
                logger.info(f"下降发现卖点")
                logger.info(f"下降卖点: {buyin_price}")
                logger.info(f"下降卖点参考数据")
                logger.info(f"k1={k1} k2= {k2} k3={data['k']}")
                logger.info(f"m1={m1} m2={data['m']}")
                logger.info(f"d1={d1} d2={data['d']}")
                break
        except Exception as e:
            logger.error(e)
            break



        
        

                               








                        





    
    
                

