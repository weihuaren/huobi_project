import logging
import json
import pandas as pd
from .swap import get_klines
from .util import get_logger

logger = get_logger('indicators')

def get_indicators():
    try: 
        data = []
        klines = get_klines()
        for kline in klines:
            data.append({'close': kline['close'], 'volume': kline['vol'], 'high': kline['high'], 'low': kline['low']})
        df = pd.DataFrame.from_dict(data)
        df['ema12'] = pd.Series.ewm(df['close'], span=12).mean()
        df['ema26'] = pd.Series.ewm(df['close'], span=26).mean()
        df['dif']= df['ema12'] - df['ema26']
        df['dea']= pd.Series.ewm(df['dif'], span=9).mean()
        df['histogram']= df['dif'] - df['dea']
        df['ma20_volume'] = df['volume'].rolling(window=20).mean()
        df['ma15_close'] = df['close'].rolling(window=15).mean()
        return {
            'v': df['volume'].iloc[-1],
            'ma20_volume': df['ma20_volume'].iloc[-1],
            'k': df['close'].iloc[-1],
            'ma15_close': df['ma15_close'].iloc[-1],
            'd': df['dif'].iloc[-1],
            'm': df['histogram'].iloc[-1],
            'dea': df['dea'].iloc[-1],
            'previous_histogram': df['histogram'].iloc[-2],
            'high_k_last_40': df['high'].tail(40).max(),
            'low_k_last_40': df['low'].tail(40).min(),
        }
    except Exception as e:
        logger.error(e)
        return 'error'


