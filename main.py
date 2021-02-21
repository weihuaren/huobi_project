import logging
import schedule
import time
from src.algorithm import run
from src.util import get_logger

logger = get_logger('main')

if __name__ == '__main__':
    logger.info('this is main')
    run()
    # schedule.every(10).seconds.do(run)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    