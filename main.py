import logging
from src.algorithm import run_strategy, test_run
from src.util import get_logger

logger = get_logger('main')

if __name__ == '__main__':
    logger.info('program started')
    # test_run()
    while True:
        try:
            run_strategy()
        except Exception as e:
            logger.error(e)