import json
import time
from .util import get_logger
from .indicators import get_indicators
from .swap import close_positions, get_all_positions, open, fund, LEVERAGE_RATE
logger = get_logger('algorithm')

def long_strategy():
    close_positions(get_all_positions())
    m1 = None
    d1 = None
    k1 = None
    k1_min = None
    k2 = None
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
            and data['k'] < k1 \
            and data['v'] > 2.5*data['average_v']:
                k2 = data['k']
                logger.info(f"long strategy open buy positions")
                current_fund = fund()
                open(current_fund*0.2/(k2/1000)*LEVERAGE_RATE, 'buy')
                logger.info(f"k1={k1} k2={data['k']}")
                logger.info(f"m1={m1} m2={data['m']}")
                logger.info(f"d1={d1} d2={data['d']}")
                continue

            if k2 and data['k'] < k2*0.994:
                logger.info(f"long strategy force close positions to prevent further loss")
                close_positions(get_all_positions())
                break
            if k2 \
            and (data['d'] > 0 \
            or data['d'] < d1 \
            or data['k'] < 0.9*k2):
                k2 = data['k']
                logger.info(f"long strategy close positions")
                close_positions(get_all_positions())
                logger.info(f"k1={k1} k2= {k2} k3={data['k']}")
                logger.info(f"m1={m1} m2={data['m']}")
                logger.info(f"d1={d1} d2={data['d']}")
                break
        except Exception as e:
            logger.error(e)
            break


        
        

                               








                        





    
    
                

