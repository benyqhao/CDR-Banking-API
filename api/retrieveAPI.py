
import json
import logging
import requests
from . import parseItems

def call(url, version):
    try:
        response = requests.get(url, headers={'User-Agent': 'Python/3.11.1', 'Accept':'application/json', 'x-v': f'{version}'})
        if response.status_code == 200:
            logging.info(f'{response.status_code} - {url} success; opened')
            return response.json()
        elif version <= 5:
            logging.warning(f'HTTP {response.status_code} Response - {url} failed; {version} x-v failed')
            version += 1
            return call(url, version)
        else:
            logging.error(f'{response.status_code} - {url} failed')
    except Exception as error:
        logging.warning(error)

def handleCall(json, handleType, providerId, productId):
    try:
        parse_json = json['data']
        if handleType == 'provider':
            parseItems.parseProviders(parse_json)
        if handleType == 'product':
            parseItems.parseProducts(parse_json, providerId)
        if handleType == 'productDetails':
            parseItems.parseProductDetails(parse_json, providerId, productId)
    except Exception as error:
        logging.critical(error)
    return