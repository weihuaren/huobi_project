import logging
import json
import sys
def get_logger(name):
    logging.basicConfig(stream=sys.stdout,
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.INFO)
    return logging.getLogger(name)

def get_configs():
    with open('config.json') as json_file:
        return json.load(json_file)