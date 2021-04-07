import requests
from urllib import parse
import json
from datetime import datetime
import hmac
import base64
from hashlib import sha256

ACCESS_KEY = ''
ACCESS_SECRET = ''

CONTRACT_CODE = 'BTC-USDT'
HOST = 'api.hbdm.com'

def main(event, context):
    close_positions(get_all_positions())

def close(volume, direction):
    data = {
        "contract_code": CONTRACT_CODE,
        "direction": direction,
        "offset": 'close',
        "volume": int(volume),
    }
    result = post(ACCESS_KEY, ACCESS_SECRET, HOST, '/linear-swap-api/v1/swap_cross_lightning_close_position', data=data)
    if result['status'] and result['status'] == 'ok':
        print(f'close position {data}')
        return result
    else: 
        print(result)
        print('cannot close position via API, please check urgently!')
        raise Exception(result)

def get_all_positions():
    result = post(ACCESS_KEY, ACCESS_SECRET, HOST, '/linear-swap-api/v1/swap_cross_position_info', data={
        "contract_code": CONTRACT_CODE,
    })
    if result['status'] and result['status'] == 'ok':
        return result['data']
    else:
        print("cannot get account position")
        raise Exception("cannot get account position")

def close_positions(positions):
    for position in positions:
        if position['direction'] == 'buy':
            close(position['volume'], 'sell')
        if position['direction'] == 'sell':
            close(position['volume'], 'buy')
    print(f'all position closed {positions}')

def _get_url_suffix(method:str, access_key:str, secret_key:str, host:str, path:str)->str:
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    timestamp = parse.quote(timestamp)
    suffix = 'AccessKeyId={}&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp={}'.format(access_key, timestamp)
    payload = '{}\n{}\n{}\n{}'.format(method.upper(), host, path, suffix)

    digest = hmac.new(secret_key.encode('utf8'), payload.encode('utf8'), digestmod=sha256).digest()
    signature = base64.b64encode(digest).decode()

    suffix = '{}&Signature={}'.format(suffix, parse.quote(signature))
    return suffix

def post(access_key:str, secret_key:str, host:str, path:str, data:dict = None)->json:
    try:
        url = 'https://{}{}?{}'.format(host, path, _get_url_suffix('post', access_key, secret_key, host, path))
        headers = {'Accept':'application/json', 'Content-type':'application/json'}
        res = requests.post(url, json=data, headers = headers)
        data = res.json()
        return data
    except Exception as e:
        raise Exception(e)

main('', '')