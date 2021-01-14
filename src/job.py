import logging
import json
from huobi.client.account import AccountClient
from huobi.constant import *

def trade():
    with open('clients.json') as json_file: 
        clients = json.load(json_file)
        for client in clients:
            logging.info(client)
            account_client = AccountClient(api_key=client["api_key"], secret_key=client["secret_key"])
            account_balance_list = account_client.get_account_balance()
            if account_balance_list and len(account_balance_list):
                    for account_obj in account_balance_list:
                        account_obj.print_object()

trade()

