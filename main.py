import logging
import schedule
import time
from src.algorithm import run
logging.basicConfig(handlers=[logging.FileHandler(filename="tradelog.txt", 
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.INFO)

if __name__ == '__main__':
    run()
    # schedule.every(10).seconds.do(run)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    