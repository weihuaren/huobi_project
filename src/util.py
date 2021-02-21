import logging

def get_logger(name):
    logging.basicConfig(handlers=[logging.FileHandler(filename="tradelog.txt", 
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.DEBUG)
    return logging.getLogger(name)