import logging
import schedule
import time
from src.job import trade
logging.basicConfig(format='%(asctime)s %(message)s', filename='huobi_project.log', filemode='w', level=logging.DEBUG)

if __name__ == '__main__':
    schedule.every(10).seconds.do(trade)
    while True:
        schedule.run_pending()
        time.sleep(1)

    