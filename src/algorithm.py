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

    # market trend
    high_k_last_40 = None
    low_k_last_40 = None
    high_k_last_40_open = None
    low_k_last_40_open = None
    trend_k = None
    trend_strategy = False
    trend_direction = None

    while True:
        time.sleep(1)
        try :
            
            data = get_indicators()
            if data == 'error':
                continue

            high_k_last_40 = data['high_k_last_40']
            low_k_last_40 = data['low_k_last_40']

            logger.info(f'k:{data["k"]} k:{data["open"]} low:{data["low"]} high:{data["high"]} trend_strategy:{trend_strategy} trend_k:{trend_k} high_k_last_40:{high_k_last_40} low_k_last_40:{low_k_last_40} trend_direction:{trend_direction} ')

            # market trend
            if high_k_last_40 - low_k_last_40 <= 200:
                trend_strategy = True
                if k2:
                    close_positions(get_all_positions())
                    break
                if not trend_k and data["k"] > low_k_last_40 + 210:
                    high_k_last_40_open = high_k_last_40
                    low_k_last_40_open = low_k_last_40
                    trend_k = data['k']
                    trend_direction = 'buy'
                    current_fund = fund()
                    open(current_fund*0.2/(trend_k/1000)*LEVERAGE_RATE, trend_direction)
                    logger.info(f"open buy positions trend_k={trend_k}")
                    continue
                if not trend_k and data["k"] < high_k_last_40 - 210:
                    high_k_last_40_open = high_k_last_40
                    low_k_last_40_open = low_k_last_40
                    trend_k = data['k']
                    trend_direction = 'sell'
                    current_fund = fund()
                    open(current_fund*0.2/(trend_k/1000)*LEVERAGE_RATE, trend_direction)
                    logger.info(f"open buy positions trend_k={trend_k}")
                    continue
            else:
                trend_strategy = False

            if trend_k:
                if (trend_direction == 'buy' and ((data['k'] <= data['ma15_close'] and data['k'] > low_k_last_40_open + 210) or data['k'] < low_k_last_40_open)) \
                or (trend_direction == 'sell' and ((data['k'] >= data['ma15_close'] and data['k'] < high_k_last_40_open - 210) or data['k'] > high_k_last_40_open)):
                    close_positions(get_all_positions())
                    break

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
            if not trend_strategy and not trend_k and direction == 'buy' and (not k2) and m1 and d1 and k1 \
            and (d1 < m1) \
            and data['m'] > m1 \
            and data['d'] > d1 \
            and data['d'] < data['m'] \
            and data['low'] < k1 \
            and data['open'] > (data['high'] + data['low'])/2 \
            and data['close'] > (data['high'] + data['low'])/2 \
            and data['v'] > 3*data['ma20_volume']:
                k2 = data['k']
                current_fund = fund()
                open(current_fund*0.2/(k2/1000)*LEVERAGE_RATE, direction)
                logger.info(f"open {direction} positions k1={k1} k2={data['k']} m1={m1} m2={data['m']} d1={d1} d2={data['d']}")
                continue

            #sell
            if not trend_strategy and not trend_k and direction == 'sell' and (not k2) and m1 and d1 and k1 \
            and (d1 > m1) \
            and data['m'] < m1 \
            and data['d'] < d1 \
            and data['d'] > data['m'] \
            and data['high'] > k1 \
            and data['open'] < (data['high'] + data['low'])/2 \
            and data['close'] < (data['high'] + data['low'])/2 \
            and data['v'] > 3*data['ma20_volume']:
                k2 = data['k']
                current_fund = fund()
                open(current_fund*0.2/(k2/1000)*LEVERAGE_RATE, direction)
                logger.info(f"open {direction} positions k1={k1} k2={data['k']} m1={m1} m2={data['m']} d1={d1} d2={data['d']}")
                continue
            
            #buy
            if direction == 'buy' and k2 \
            and (data['d'] > 10 or data['k'] < 0.995*k2 or data['k'] < data['low']):
                k2 = data['k']
                close_positions(get_all_positions())
                logger.info(f"close positions k1={k1} k2= {k2} k3={data['k']} m1={m1} m2={data['m']} d1={d1} d2={data['d']}")
                break

            #sell
            if direction == 'sell' and k2 \
            and (data['d'] < -10 or data['k'] > 1.005*k2 or data['k'] > data['high']):
                k2 = data['k']
                close_positions(get_all_positions())
                logger.info(f"close positions k1={k1} k2= {k2} k3={data['k']} m1={m1} m2={data['m']} d1={d1} d2={data['d']}")
                break

        except Exception as e:
            logger.error(e)
            break