import logging
import json
import time
from huobi.constant import *
from .client import MyAccountClient
from huobi.client.market import MarketClient
from huobi.utils import *
from .indicators import get_indicators
from pprint import pprint

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

client = MyAccountClient()
market_client = MarketClient()

def run():
    logging.info("开始运行程序")
    logging.info("开始取K1")
    buyin_price = None    
    continue_trade = True
    k1 = None
    m1 = None
    d1 = None  
    d1_15 = None  
    while not k1:
        time.sleep(1)
        indicators_min5 = get_indicators(CandlestickInterval.MIN5)
        indicators_min15 = get_indicators(CandlestickInterval.MIN15)
        indicators_min60 = get_indicators(CandlestickInterval.MIN60)
        indicators_min240 = get_indicators(CandlestickInterval.HOUR4)
        
        # if: (5v >= 4*5vj) 
        # && (15v >= 4*15vj) 
        # && (5d < 5m) 
        # && (15d < 15m) 
        # && (current 60m > previous 60m) 
        # && (current 240m > previous 240m)
        if (indicators_min5['volume'] >= 4*indicators_min5['average_volume']) \
        and (indicators_min15['volume'] >= 4*indicators_min15['average_volume']) \
        and (indicators_min5['dif'] < indicators_min5['histogram']) \
        and (indicators_min15['dif'] < indicators_min15['histogram']) \
        and (indicators_min60['histogram'] > indicators_min60['previous_histogram']) \
        and (indicators_min240['histogram'] > indicators_min240['previous_histogram']):
            k1 = indicators_min5['close']
            m1 = indicators_min5['histogram']
            m1_15 = indicators_min15['histogram']
            d1 = indicators_min5['dif']
            d1_15 = indicators_min15['dif']
            logging.info(f'k1取得 k1={k1} m1={m1} d1={d1} d1_15={d1_15}')
            logging.info("以下为满足k1条件的数据参考")
            logging.info("满足k1条件的5分钟数据")
            logging.info(indicators_min5)
            logging.info("满足k1条件的15分钟数据")
            logging.info(indicators_min15)
            logging.info("满足k1条件的60分钟数据")
            logging.info(indicators_min60)
            logging.info("满足k1条件的4小时数据")
            logging.info(indicators_min240)
            buyin_price = market_client.get_market_trade(symbol="btcusdt")[0].price
            logging.info(f'买入 价格 {buyin_price}')

 
    k2 = None
    while not k2:
        logging.info("开始取K2")
        time.sleep(1)
        current_price = market_client.get_market_trade(symbol="btcusdt")[0].price
        if current_price < 0.94*buyin_price:
            continue_trade = False
            logging.info(f"平仓止损 买入价格 {buyin_price} 卖出价格 {current_price}")
            break
        indicators_min5 = get_indicators(CandlestickInterval.MIN5)
        # if:k2=80%5j20 (+- 0.5%)
        if 0.8*indicators_min5['average_close']*0.995 <= indicators_min5['close'] <= 0.8*indicators_min5['average_close']*1.005:
            k2 = indicators_min5['close']
            logging.info(f'k2取得 k2={k2}')
            logging.info("以下为满足k2条件的数据参考")
            logging.info("满足k2条件的5分钟数据")
            logging.info(indicators_min5)            
            logging.info(f"平仓 买入价格 {buyin_price} 卖出价格 {current_price}")

    k3 = None
    while not k3 and continue_trade:
        logging.info("开始取K3")
        time.sleep(1)
        indicators_min5 = get_indicators(CandlestickInterval.MIN5)
        indicators_min15 = get_indicators(CandlestickInterval.MIN15)
        indicators_min60 = get_indicators(CandlestickInterval.MIN60)
        indicators_min240 = get_indicators(CandlestickInterval.HOUR4)
        # if (5v>=2*5vj) 
        # && (15v>=90%15vj）
        # && (k3 = 0.8*k1)
        # && (5d > 5d1)
        # && (15d > 15d1)
        # && (5m > 5m1)
        # && (15m > 15m1)
        # && (当下k线60m>前一根k线60m)
        # && (当下k线240m>前一根k线240m)
        if (indicators_min5['volume'] >= 2*indicators_min5['average_volume']) \
        and (indicators_min15['volume'] >= 0.9*indicators_min15['average_volume']) \
        and (0.8*k1*0.995 <= indicators_min5['close'] <= 0.8*k1*1.005) \
        and (indicators_min5['dif'] > d1) \
        and (indicators_min15['dif'] > d1_15) \
        and (indicators_min5['histogram'] > m1) \
        and (indicators_min15['histogram'] > m1_15) \
        and (indicators_min60['histogram'] > indicators_min60['previous_histogram']) \
        and (indicators_min240['histogram'] > indicators_min240['previous_histogram']):
            k3 = indicators_min5['close']
            logging.info(f'k3取得 k3={k3}')
            logging.info("以下为满足k3条件的数据参考")
            logging.info("满足k3条件的5分钟数据")
            logging.info(indicators_min5)
            logging.info("满足k3条件的15分钟数据")
            logging.info(indicators_min15)
            logging.info("满足k3条件的60分钟数据")
            logging.info(indicators_min60)
            logging.info("满足k3条件的4小时数据")
            logging.info(indicators_min240)        
            buyin_price = market_client.get_market_trade(symbol="btcusdt")[0].price
            logging.info(f'买入 价格 {buyin_price}')

    k4 = None
    ifSell = False
    m4 = None
    d4 = None    
    while continue_trade:

        logging.info("开始取K4")
        current_price = market_client.get_market_trade(symbol="btcusdt")[0].price
        if current_price < 0.94*buyin_price:
            continue_trade = False
            logging.info(f"平仓止损 买入价格 {buyin_price} 卖出价格 {current_price}")
            break
        time.sleep(1)
        indicators_min5 = get_indicators(CandlestickInterval.MIN5)

        if not K4 or indicators_min5['close'] < 0:
            logging.info(f'k4 负值 k4={k4}')
            K4 = indicators_min5['close']
            m4 = indicators_min5['histogram']
            d4 = indicators_min5['dif']
        elif k4 and k4 < 0 and indicators_min5['close'] > 0:
            logging.info(f'k4 负值变正值 k4={k4}')
            K4 = indicators_min5['close']
            m4 = indicators_min5['histogram']
            d4 = indicators_min5['dif']
        elif k4 and k4 > 0 and indicators_min5['close'] > 0:
            if indicators_min5['close'] >= k4:
                logging.info(f'新的k4最大值 k4={k4}')
                K4 = indicators_min5['close']
                m4 = indicators_min5['histogram']
                d4 = indicators_min5['dif']
            elif indicators_min5['close'] < k4:
                logging.info(f'价格下跌 k={indicators_min5["close"]} k4={k4}')
                logging.info('开始寻找平仓点位')
                ifSell = True

        if ifSell and (indicators_min5['close'] > indicators_min5['close_average_ma10'])\
        and (indicators_min5['histogram'] < m4) \
        and (indicators_min5['dif'] < d4):
            logging.info(f"满足k4平仓条件 k4={k4} m4={m4} d4={d4}")
            logging.info("以下为满足k4条件的数据参考")
            logging.info("满足k4条件的5分钟数据")
            logging.info(indicators_min5)
            logging.info(f"平仓 买入价格 {buyin_price} 卖出价格 {current_price}")
            logging.info("交易结束")
            break

                               








                        





    
    
                

