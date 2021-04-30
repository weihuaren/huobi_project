import json
import time
from .util import get_logger
from .indicators import get_indicators
from .swap import close_positions, get_all_positions, open, fund, LEVERAGE_RATE

macd_logger = get_logger('macd_strategy')
trend_logger = get_logger('trend_strategy')

def macd_strategy():    
    close_positions(get_all_positions())
    m1 = None
    d1 = None
    l1 = None
    h1 = None
    allow_buy = False
    buy_price = None
    direction = None
    while True:
        time.sleep(1)
        try :
            data = get_indicators()
            if data == 'error':
                continue

            # log data
            macd_logger.info(data)
            macd_logger.info(f'm1:{m1} d1:{d1} l1:{l1} h1:{h1} direction:{direction} allow_buy:{allow_buy} buy_price:{buy_price}')

            # don't open position in macd strategy when trend strategy condition is met
            if data['h_last_30'] - data['l_last_30'] <= 400:
                allow_buy = False
                if buy_price:
                    close_positions(get_all_positions())
                    break
            else:
                allow_buy = True

            # open buy
            if (data['m'] < 0 ) and (data['d'] < 0):
                m1 = min(data['m'], m1) if m1 else data['m']
                d1 = min(data['d'], d1) if d1 else data['d']
                l1 = min(data['l'], l1) if l1 else data['l']
                h1 = None
            
            # open sell
            if (data['m'] > 0 ) and (data['d'] > 0):
                m1 = max(data['m'], m1) if m1 else data['m']
                d1 = max(data['d'], d1) if d1 else data['d']
                h1 = max(data['h'], h1) if h1 else data['h']
                l1 = None

            # open buy
            if allow_buy and not buy_price and l1 \
            and d1 < m1 \
            and data['m'] > m1 \
            and data['d'] > d1 \
            and data['l'] < l1 \
            and data['v'] > 3*data['v_20ma'] \
            and data['o'] > (data['h']+data['l'])/2 \
            and data['k'] > (data['h']+data['l'])/2:
                direction = 'buy'
                buy_price = data['k']
                current_fund = fund()
                open(current_fund*0.2/(buy_price/1000)*LEVERAGE_RATE, 'buy')
                continue

            # open sell
            if allow_buy and not buy_price and h1 \
            and d1 > m1 \
            and data['m'] < m1 \
            and data['d'] < d1 \
            and data['h'] > h1 \
            and data['v'] > 3*data['v_20ma'] \
            and data['o'] < (data['h']+data['l'])/2 \
            and data['k'] < (data['h']+data['l'])/2:
                direction = 'sell'
                buy_price = data['k']
                current_fund = fund()
                open(current_fund*0.2/(buy_price/1000)*LEVERAGE_RATE, 'sell')
                continue

            # close buy
            if buy_price and direction == 'buy'\
            and (data['d'] > 10 or data['k'] <= buy_price*0.995 or data['k'] < l1):
                 close_positions(get_all_positions())
                 break

            # close sell
            if buy_price and direction == 'sell'\
            and (data['d'] < -10 or data['k'] >= buy_price*1.005 or data['k'] > h1):
                 close_positions(get_all_positions())
                 break
            
        except Exception as e:
            macd_logger.error(e)
            break

def trend_strategy():
    close_positions(get_all_positions())
    buy_price = None
    buy_timestamp = None
    direction = None
    h_last_30 = None
    l_last_30 = None
    while True:
        time.sleep(1)
        try :
            time_now = time.time()
            data = get_indicators()

            if data == 'error':
                continue
            # log data
            trend_logger.info(f'buy_price:{buy_price} direction:{direction}')
            trend_logger.info(data)
            if not buy_price and data['h_last_30'] - data['l_last_30'] <= 400:
                if data['k'] > data['h_last_30'] + 10:
                    direction = 'buy'
                    buy_timestamp = time.time()
                    h_last_30 = data['h_last_30']
                    l_last_30 = data['l_last_30']
                    buy_price = data['k']
                    current_fund = fund()
                    open(current_fund*0.2/(buy_price/1000)*LEVERAGE_RATE, 'buy')
                    continue
                elif data['k'] < data['l_last_30'] - 10:
                    direction = 'sell'
                    buy_timestamp = time.time()
                    h_last_30 = data['h_last_30']
                    l_last_30 = data['l_last_30']
                    buy_price = data['k']
                    current_fund = fund()
                    open(current_fund*0.2/(buy_price/1000)*LEVERAGE_RATE, 'sell')
                    continue

            if buy_price and direction == 'buy':
                if (data['k'] <= data['k_15ma'] and data['k'] > h_last_30) \
                or data['k'] < l_last_30 \
                or time_now - buy_timestamp > 60*20:
                    close_positions(get_all_positions())
                    break
                
            if buy_price and direction == 'sell':
                if (data['k'] >= data['k_15ma'] and data['k'] < l_last_30) \
                or data['k'] > h_last_30 \
                or time_now - buy_timestamp > 60*20:
                    close_positions(get_all_positions())
                    break
        except Exception as e:
            trend_logger.error(e)
            break