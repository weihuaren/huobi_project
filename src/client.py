from huobi.client.account import AccountClient
import json

def MyAccountClient():
    with open('key.json') as json_file:
        credentials = json.load(json_file)
        return AccountClient(api_key=credentials["api_key"], secret_key=credentials["secret_key"])

