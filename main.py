import logging
import schedule
import time
from src.algorithm import run
logging.basicConfig(format='%(asctime)s %(message)s', filename='huobi_project.log', filemode='w', level=logging.DEBUG)

if __name__ == '__main__':
    run()
    # schedule.every(10).seconds.do(run)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    