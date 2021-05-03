import logging
import os
from src.swap import close_positions, get_all_positions, open, fund, LEVERAGE_RATE
from src.algorithm import macd_strategy, trend_strategy
from src.util import get_logger

logger = get_logger('main')

if __name__ == '__main__':
    close_positions(get_all_positions())
    strategy = os.environ['strategy']
    logger.info(f'{strategy} strategy started')
    if strategy == 'macd':
        while True:
            try:
                macd_strategy()
            except Exception as e:
                logger.error(e)
    elif strategy == 'trend' or strategy == 'trend-ethusdt' or strategy == 'trend-mdxusdt':
        while True:
            try:
                trend_strategy()
            except Exception as e:
                logger.error(e)
    else:
        print('please pick a strategy first')