import logging
import os
from src.algorithm import macd_strategy
from src.util import get_logger

logger = get_logger('main')

if __name__ == '__main__':
    strategy = os.environ['strategy']
    logger.info(f'{strategy} strategy started')
    if strategy == 'macd':
        while True:
            try:
                macd_strategy()
            except Exception as e:
                logger.error(e)
    elif strategy == 'trend':
        print("trend strategy is currently under development")
    else:
        print('please pick a strategy first')