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
            data.append({'close': kline['close'], 'volume': kline['vol'], 'high': kline['high'], 'low': kline['low'], 'open': kline['open']})
        df = pd.DataFrame.from_dict(data)
        df['ema12'] = pd.Series.ewm(df['close'], span=12).mean()
        df['ema26'] = pd.Series.ewm(df['close'], span=26).mean()
        df['dif']= df['ema12'] - df['ema26']
        df['dea']= pd.Series.ewm(df['dif'], span=9).mean()
        df['histogram']= df['dif'] - df['dea']
        df['v_20ma'] = df['volume'].rolling(window=20).mean()
        df['ma15_close'] = df['close'].rolling(window=9).mean()
        df['ma_high'] = df['high'].rolling(window=5).mean()
        df['ma_low'] = df['low'].rolling(window=5).mean()
        return {
            'v': df['volume'].iloc[-1],
            'v_20ma': df['v_20ma'].iloc[-1],
            'k': df['close'].iloc[-1],
            'o': df['open'].iloc[-1],
            'h': df['high'].iloc[-1],
            'l': df['low'].iloc[-1],
            'k_15ma': df['ma15_close'].iloc[-1],
            'h_ma': df['ma_high'].iloc[-1],
            'l_ma': df['ma_low'].iloc[-1],
            'd': df['dif'].iloc[-1],
            'm': df['histogram'].iloc[-1],
            'dea': df['dea'].iloc[-1],
            'previous_histogram': df['histogram'].iloc[-2],
            'h_last_30': df['high'][:-1].tail(30).max(),
            'l_last_30': df['low'][:-1].tail(30).min(),
        }
    except Exception as e:
        logger.error(e)
        return 'error'


