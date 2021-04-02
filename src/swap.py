import requests
import json
from .auth import post
from .util import get_configs, get_logger

logger = get_logger('futures')

configs = get_configs()
CONTRACT_CODE = configs["contract_code"]
HOST = configs["host"]
ACCESS_KEY = configs["api_key"]
ACCESS_SECRET = configs["secret_key"]
LEVERAGE_RATE = configs["leverage_rate"]

def get_klines(contract_code=CONTRACT_CODE, period='1min', size=200):
    try :
        r = requests.get(f'https://{HOST}/linear-swap-ex/market/history/kline?period={period}&size={size}&contract_code={contract_code}')
        return r.json()['data']
    except Exception as e:
        logger.error(e)

# example open(1, 'buy') open(2, 'sell')
def open(volume, direction):
    data={
        "contract_code": CONTRACT_CODE,
        "direction": direction,
        "offset": 'open',
        "lever_rate": LEVERAGE_RATE,
        "volume": int(volume) if volume >=1 else 1,
        "order_price_type":"opponent_ioc",
    }
    result = post(ACCESS_KEY, ACCESS_SECRET, HOST, '/linear-swap-api/v1/swap_cross_order', data=data)
    if result['status'] and result['status'] == 'ok':
        logger.info(f'open position {data}')
        return result
    else: 
        logger.error(result)
        raise Exception(result)

# example close(1, 'buy') close(2, 'sell')
def close(volume, direction):
    data = {
        "contract_code": CONTRACT_CODE,
        "direction": direction,
        "offset": 'close',
        "volume": int(volume),
    }
    result = post(ACCESS_KEY, ACCESS_SECRET, HOST, '/linear-swap-api/v1/swap_cross_lightning_close_position', data=data)
    if result['status'] and result['status'] == 'ok':
        logger.info(f'close position {data}')
        return result
    else: 
        logger.error(result)
        logger.error('cannot close position via API, please check urgently!')
        raise Exception(result)

def fund():
    result = post(ACCESS_KEY, ACCESS_SECRET, HOST, '/linear-swap-api/v1/swap_balance_valuation', data={
        "valuation_asset": "USDT",
    })
    if result != None and result['data'][0]['valuation_asset'] == 'USDT':
        return int(float((result['data'][0]['balance'])))
    else:
        logger.error("cannot get account fund information")
        raise Exception("cannot get account fund information")
        
def get_all_positions():
    result = post(ACCESS_KEY, ACCESS_SECRET, HOST, '/linear-swap-api/v1/swap_cross_position_info', data={
        "contract_code": CONTRACT_CODE,
    })
    if result['status'] and result['status'] == 'ok':
        return result['data']
    else:
        logger.error("cannot get account position")
        raise Exception("cannot get account position")

def get_long_positions_only():
    all_positions = get_all_positions()
    return list(filter(lambda x: x['direction'] == 'buy', all_positions))

def get_short_positions_only():
    all_positions = get_all_positions()
    return list(filter(lambda x: x['direction'] == 'sell', all_positions))

def close_positions(positions):
    for position in positions:
        if position['direction'] == 'buy':
            close(position['volume'], 'sell')
        if position['direction'] == 'sell':
            close(position['volume'], 'buy')
    logger.info(f'all position closed {positions}')

