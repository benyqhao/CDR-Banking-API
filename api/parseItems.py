import os
import json
import logging

# https://stackoverflow.com/a/25851972/9389353
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
    
def parseProviders(jsonfile):
    try:
        output = {}
        for provider in jsonfile:
            providerId = ""
            if ('dataHolderBrandId' in provider or 'interimId' in provider):
                if ('dataHolderBrandId' in provider):
                    providerId = provider['dataHolderBrandId']
                else:
                    providerId = provider['interimId']
                output[providerId] = {}
                if 'dataHolderBrandId' in provider:
                    output[providerId]['dataHolderBrandId'] = provider['dataHolderBrandId']
                if 'interimId' in provider:
                    output[providerId]['interimId'] = provider['interimId']
                output[providerId]['brandName'] = provider['brandName']
                output[providerId]['logoUri'] = provider['logoUri']
                output[providerId]['publicBaseUri'] = provider['publicBaseUri']
                output[providerId]['lastUpdated'] = provider['lastUpdated']
                if 'abn' in provider:
                    output[providerId]['abn'] = provider['abn']
                if 'acn' in provider:
                    output[providerId]['acn'] = provider['acn']
                if 'arbn' in provider:
                    output[providerId]['arbn'] = provider['arbn']
        with open("./src/providers/providers.json", "w") as outfile:
            json.dump(output, outfile, indent = 4)
            outfile.close()
    except Exception as error:
        logging.critical(error)
    return

def parseProducts(jsonfile, providerId):
    try:
        update_record = True
        directory = './src/providers/products/'
        try:
            for file in os.listdir({directory}):
                if file == providerId:
                    with open(f'{directory}{file}', "r") as original_json:
                        json_to_compare = json.load(original_json)
                        original_json.close()
                    if ordered(jsonfile) == ordered(json_to_compare):
                        update_record == False
        except Exception as error:
            logging.warning({error})
        if update_record and len(jsonfile) != 0:
            with open(f'{directory}{providerId}.json', "w") as json_output:
                json.dump(jsonfile, json_output, indent = 4)
                json_output.close()
    except Exception as error:
        logging.critical(error)
    return

def parseProductDetails(jsonfile, providerId, productId):
    try:
        update_record = True
        directory = f'./src/providers/productDetails/{providerId}'
        try:
            for file in os.listdir(directory):
                if file == f'{productId}.json':
                    with open(f'{directory}/{file}.json', "r") as original_json:
                        json_to_compare = json.load(original_json)
                        original_json.close()
                    if ordered(jsonfile) == ordered(json_to_compare):
                        update_record == False
        except Exception as error:
            logging.warning({error})
        if update_record and len(jsonfile) != 0:
            with open(f'{directory}/{productId}.json', "w") as json_output:
                json.dump(jsonfile, json_output, indent = 4)
                json_output.close()
    except Exception as error:
        logging.critical(error)
    return

# def parseHistory(jsonfile):
#     pass