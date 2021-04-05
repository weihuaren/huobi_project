import json
import time
from .util import get_logger
from .indicators import get_indicators
from .swap import close_positions, get_all_positions, open, fund, LEVERAGE_RATE
logger = get_logger('algorithm')

def test_run():
    data = get_indicators()
    close_positions(get_all_positions())
    current_fund = fund()
    open(current_fund*0.2/(data['k']/1000)*LEVERAGE_RATE, 'buy')
    close_positions(get_all_positions())
    
def run_strategy():
    close_positions(get_all_positions())
    m1 = None
    d1 = None
    k1 = None
    k1_min = None
    k2 = None
    direction = None
    while True:
        time.sleep(1)
        try :
            if k1:
                logger.info(f'k1: {k1} k2: {k2} d1: {d1} m1: {m1} direction: {direction}')
            data = get_indicators()
            if data == 'error':
                continue
            #buy
            if (not k2) and (not m1) and (not d1) and (not k1) \
            and (data['m'] < 0) \
            and (data['d'] < 0):
                m1 = data['m']
                d1 = data['d']
                k1 = data['k']
                k1_min = data['k']
                direction = 'buy'
                continue

            #sell
            if (not k2) and (not m1) and (not d1) and (not k1) \
            and (data['m'] > 0) \
            and (data['d'] > 0):
                m1 = data['m']
                d1 = data['d']
                k1 = data['k']
                k1_min = data['k']
                direction = 'sell'
                continue

            #buy 
            if (not k2) and m1 and d1 and k1 \
            and direction == 'buy' \
            and data['d'] > 0:
                break

            #sell 
            if (not k2) and m1 and d1 and k1 \
            and direction == 'sell' \
            and data['d'] < 0:
                break

            #buy
            if  direction == 'buy' and m1 and d1 and k1:
                m1 = min(m1, data['m'])
                k1_min = min(k1_min, data['k'])
                if data['d'] < d1:
                    d1 =  data['d']
                    k1 = k1_min

            #sell
            if  direction == 'sell' and m1 and d1 and k1:
                m1 = max(m1, data['m'])
                k1_min = max(k1_min, data['k'])
                if data['d'] > d1:
                    d1 =  data['d']
                    k1 = k1_min

            #buy
            if direction == 'buy' and (not k2) and m1 and d1 and k1 \
            and (d1 < m1) \
            and data['m'] > m1 \
            and data['d'] > d1 \
            and data['d'] < data['m'] \
            and data['k'] < k1 \
            and data['v'] > 3*data['ma20_volume']:
                k2 = data['k']
                current_fund = fund()
                open(current_fund*0.2/(k2/1000)*LEVERAGE_RATE, direction)
                logger.info(f"open {direction} positions k1={k1} k2={data['k']} m1={m1} m2={data['m']} d1={d1} d2={data['d']}")
                continue

            #sell
            if direction == 'sell' and (not k2) and m1 and d1 and k1 \
            and (d1 > m1) \
            and data['m'] < m1 \
            and data['d'] < d1 \
            and data['d'] > data['m'] \
            and data['k'] > k1 \
            and data['v'] > 3*data['ma20_volume']:
                k2 = data['k']
                current_fund = fund()
                open(current_fund*0.2/(k2/1000)*LEVERAGE_RATE, direction)
                logger.info(f"open {direction} positions k1={k1} k2={data['k']} m1={m1} m2={data['m']} d1={d1} d2={data['d']}")
                continue
            
            #buy
            if direction == 'buy' and k2 \
            and (data['d'] > 0 \
            or data['d'] < d1 \
            or data['k'] < 0.996*k2):
                k2 = data['k']
                close_positions(get_all_positions())
                logger.info(f"close positions k1={k1} k2= {k2} k3={data['k']} m1={m1} m2={data['m']} d1={d1} d2={data['d']}")
                break

            #sell
            if direction == 'sell' and k2 \
            and (data['d'] < 0 \
            or data['d'] > d1 \
            or data['k'] > 1.004*k2):
                k2 = data['k']
                close_positions(get_all_positions())
                logger.info(f"close positions k1={k1} k2= {k2} k3={data['k']} m1={m1} m2={data['m']} d1={d1} d2={data['d']}")
                break

        except Exception as e:
            logger.error(e)
            break


        
        

                               








                        





    
    
                

