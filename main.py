import os
import json
import logging
import concurrent.futures
from api import config, retrieveAPI
from functools import lru_cache
from logging.handlers import RotatingFileHandler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RotatingFileHandler("record-keep.log", maxBytes=1000000, backupCount=5)
    ]
)


@lru_cache(maxsize=None)
def call_and_handle(url, version, handle_type, provider_id, product_id):
    response = retrieveAPI.call(url, version)
    retrieveAPI.handleCall(response, handle_type, provider_id, product_id)


def build_json(url, version, handle_type, provider_id, product_id):
    try:
        call_and_handle(url, version, handle_type, provider_id, product_id)
    except Exception as error:
        logging.critical(error)


def build_products(read_json_location):
    try:
        with open(read_json_location, 'r') as json_file:
            provider_list = json.load(json_file)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for provider, data in provider_list.items():
                url = f"{data['publicBaseUri']}/cds-au/v1/banking/products?page-size=1000"
                future = executor.submit(
                    build_json, url, 3, "product", provider, None
                )
                futures.append(future)
            concurrent.futures.wait(futures)
    except Exception as error:
        logging.critical(error)


def build_product_details(read_json_location):
    try:
        provider_directory = "./src/providers/providers.json"
        write_base_directory = "./src/providers/productDetails"
        if not os.path.exists(write_base_directory):
            os.makedirs(write_base_directory)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for provider_file_name in os.listdir(read_json_location):
                provider_id = os.path.splitext(provider_file_name)[0]
                write_directory = os.path.join(write_base_directory, provider_id)
                if not os.path.exists(write_directory):
                    os.makedirs(write_directory)
                with open(
                    os.path.join(read_json_location, provider_file_name), 'r'
                ) as product_json_file:
                    product_list = json.load(product_json_file)
                for product_id in product_list['products']:
                    future = executor.submit(
                        build_product_detail,
                        provider_id,
                        provider_directory,
                        product_id
                    )
                    futures.append(future)
            concurrent.futures.wait(futures)
    except Exception as error:
        logging.critical(error)


# @lru_cache(maxsize=None)
def build_product_detail(provider_id, provider_directory, product_id):
    try:
        with open(provider_directory, 'r') as provider_json_file:
            provider_list = json.load(provider_json_file)
        url = f"{provider_list[provider_id]['publicBaseUri']}/cds-au/v1/banking/products/{product_id['productId']}"
        build_json(url, 3, "productDetails", provider_id, product_id['productId'])
    except Exception as error:
        print('failed')
        logging.critical(error)


def main():
    config.setupDirs()
    buildJSON('https://api.cdr.gov.au/cdr-register/v1/banking/data-holders/brands/summary', 1, 'provider', None, None)
    buildProducts('./src/providers/providers.json')
    buildProductDetails('./src/providers/products')
    
    # Testing
    # buildJSON('https://product.api.heritage.com.au/cds-au/v1/banking/products?page-size=1000', 3, 'product', 'test', None)
    # buildJSON('https://digital-api.banksa.com.au/cds-au/v1/banking/products/BSACCAmplifySignaturecardRewards', 4, 'productDetails', 'test', 'BSACCAmplifySignaturecardRewards')
    # buildJSON('https://ib.bankvic.com.au/openbanking/cds-au/v1/banking/products/S40_Savings_SMSF', 3, 'productDetails', '01608f70-e4ae-eb11-a822-000d3a884a20', 'S40_Savings_SMSF')


if __name__ == '__main__':
    main()
