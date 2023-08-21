import os
import json
import logging
from api import config, retrieveAPI

logging.basicConfig(
    level=logging.INFO
    , format="%(asctime)s, %(levelname)s %(message)s"
    , datefmt="%Y-%m-%d %H:%M:%S"
    , filename="record-keep.log"
    )

def buildJSON(url, version, handleType, providerId, productId):
    try:
        response = retrieveAPI.call(url, version)
        retrieveAPI.handleCall(response, handleType, providerId, productId)
    except Exception as error:
        logging.critical(error)

def buildProducts(read_json_location):
    try:
        with open(read_json_location, 'r') as jsonfile:
            providerList = json.load(jsonfile)
            jsonfile.close()
        for provider in providerList:
            url = f'{providerList[provider]["publicBaseUri"]}/cds-au/v1/banking/products?page-size=1000'
            buildJSON(url, 3, 'product', provider, None)
            # break
    except Exception as error:
        logging.critical(error)

def buildProductDetails(read_json_location):
    try:
        for providerFileName in os.listdir(read_json_location):
            providerId = os.path.splitext(providerFileName)[0]
            provider_directory = './src/providers/providers.json'
            write_directory = f'./src/providers/productDetails/{providerId}'
            if not os.path.exists(write_directory):
                os.makedirs(write_directory)
            with open(f'{read_json_location}/{providerFileName}', 'r') as product_jsonfile:
                productList = json.load(product_jsonfile)
                product_jsonfile.close()
            for productId in productList['products']:
                try:
                    with open(provider_directory, 'r') as provider_jsonfile:
                        providerList = json.load(provider_jsonfile)
                        provider_jsonfile.close()
                    
                    url = f"{providerList[providerId]['publicBaseUri']}/cds-au/v1/banking/products/{productId['productId']}"
                    buildJSON(url, 3, 'productDetails', providerId, productId['productId'])
                except Exception as error:
                    logging.critical(error)
            #     break
            # break
    except Exception as error:
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