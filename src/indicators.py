import logging
import json
from huobi.constant import *
from huobi.client.market import MarketClient
from huobi.utils import *
from .client import MyAccountClient
import pandas as pd
from .futures import get_klines
from src.util import get_logger

logger = get_logger('indicators')

client = MyAccountClient()
market_client = MarketClient()

def get_indicators():
    try: 
        data = []
        klines = get_klines()
        for kline in klines:
            data.append({'close': kline['close'], 'volume': kline['vol']})
        df = pd.DataFrame.from_dict(data)
        df['ema12'] = pd.Series.ewm(df['close'], span=12).mean()
        df['ema26'] = pd.Series.ewm(df['close'], span=26).mean()
        df['dif']= df['ema12'] - df['ema26']
        df['dea']= pd.Series.ewm(df['dif'], span=9).mean()
        df['histogram']= df['dif'] - df['dea']
        df['ma20_volume'] = df['volume'].rolling(window=20).mean()
        df['ma20_close'] = df['close'].rolling(window=20).mean()
        return {
            'volume': df['volume'].iloc[-1],
            'ma20_volume': df['ma20_volume'].iloc[-1],
            'k': df['close'].iloc[-1],
            'ma20_close': df['ma20_close'].iloc[-1],
            'd': df['dif'].iloc[-1],
            'm': df['histogram'].iloc[-1],
            'dea': df['dea'].iloc[-1],
            'previous_histogram': df['histogram'].iloc[-2],
        }
    except Exception as e:
        logger.error(e)
        return 'error'


