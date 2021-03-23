import logging
import schedule
import time
from src.algorithm import run_long, run_short
from src.util import get_logger
from threading import Thread

logger = get_logger('main')

if __name__ == '__main__':
    for x in range(10):
        run_long()
    # Thread(target = run_long).start()
    # Thread(target = run_short).start()
    # schedule.every(10).seconds.do(run)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    