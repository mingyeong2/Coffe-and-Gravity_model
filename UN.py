import requests
import json
import urllib.request
import pandas as pd
import sys



##country_code_setting
def country_code_setting(by_code = True):
    base_url = 'https://comtrade.un.org/data/cache/reporterAreas.json'
    r = requests.get(base_url)
    js = json.loads(r.text)
    
    countries = {}
    
    if by_code:
        for lst in js['results']:
            countries[lst['id']] = lst['text']
    else:
        for lst in js['results']:
            countries[lst['text']] = lst['id']
        
    return countries

    
    
    
    


classification_json = {
    #good default
    'HS': 'https://comtrade.un.org/data/cache/classificationHS.json',
    
    'H0': 'https://comtrade.un.org/data/cache/classificationH0.json',
    'H1':'https://comtrade.un.org/data/cache/classificationH1.json',
    'H2': 'https://comtrade.un.org/data/cache/classificationH2.json',
    'H3': 'https://comtrade.un.org/data/cache/classificationH3.json',
    'H4': 'https://comtrade.un.org/data/cache/classificationH4.json',
    'ST': 'https://comtrade.un.org/data/cache/classificationST.json',
    'S1':'https://comtrade.un.org/data/cache/classificationS1.json',
    'S2':'https://comtrade.un.org/data/cache/classificationS2.json',
    'S3':'https://comtrade.un.org/data/cache/classificationS3.json',
    'S4':'https://comtrade.un.org/data/cache/classificationS4.json',
    'BEC': 'https://comtrade.un.org/data/cache/classificationBEC.json',
    
    #service default
    'EB02': 'https://comtrade.un.org/data/cache/classificationEB02.json'
    
}


def get_class_info(classification_url = classification_json['HS']):
    r = requests.get(classification_url)
    js = json.loads(r.text)
    
    class_info = {}
    
    for info in js['results']:
        class_info[info['id']] = {'text':info['text'], 'parent':info['parent']}
    
    
    return class_info
    
    
    
def UN_availability(data_type, frequency, reporting_area, time_period, classification):
    base_url = 'http://comtrade.un.org/api//refs/da/view?'
    
    ##조건
    parameters = {'type': data_type,
                 'freq' : frequency,
                 'r' : reporting_area,
                 'ps' : time_period,
                 'px': classification}
    
    url = base_url + dict_to_string(parameters)
    print('url :', url)
    
    r = requests.get(url)
    html = r.text
    js = json.loads(html)
    
    return js 




def dict_item_to_string(key, value):
    """
    inputs: key-value pairs from a dictionary
    output: string 'key=value' or 'key=value1,value2' (if value is a list)
    examples: 'fmt', 'csv' => 'fmt=csv' or 'r', [124, 484] => 'r=124,484'
    """
    value_string = str(value) if not isinstance(value, list) else ','.join(map(str, value))
    return '='.join([key, value_string])


def dict_to_string(parameters):
    """
    input: dictionary of parameters
    output: string 'key1=value1&key2=value2&...'
    """
    param =[]
    for key, value in parameters.items():
        if value != 'any':
            param.append(dict_item_to_string(key, value))
    return '&'.join(param)


country_code_byCode = country_code_setting(True)
country_code_byLetter = country_code_setting(False)



def UN_comtrade(human_readable=False, verbose=True,
    period='recent', frequency='A', reporter=842, partner='all', product='total', tradeflow=2):
       
    base_url = 'https://comtrade.un.org/api/get?'
    
    ##조건
    fmt = 'csv' if human_readable else 'json'
    head = 'H' if human_readable else 'M'
    
    if type(reporter) == str:
        reporter = country_code_byLetter[reporter]
    
    parameters = {
            'ps': period,
            'freq': frequency,
            'r': reporter,
            'p': partner,
            'cc': product,
            'rg': tradeflow,
            'px': 'HS',      # Harmonized System (as reported) as classification scheme
            'type': 'C',     # Commodities ('S' for Services)
            'fmt': fmt,      # format of the output
            'max': 50000,    # maximum number of rows -> what happens if number of rows is bigger?
                             # https://comtrade.un.org/data/dev/portal#subscription says it is 100 000
            'head': head     # human readable headings ('H') or machine readable headings ('M')
        }
    
    url = base_url + dict_to_string(parameters)
    print('url :', url)
    
    r = requests.get(url)
    html = r.text
    js = json.loads(html)
    
    if js['validation']['message']:
        print(js['validation']['message'])
    
    print('\n# of data is', js['validation']['count']['value'])
    
    return js 





def dict_item_to_string(key, value):
    """
    inputs: key-value pairs from a dictionary
    output: string 'key=value' or 'key=value1,value2' (if value is a list)
    examples: 'fmt', 'csv' => 'fmt=csv' or 'r', [124, 484] => 'r=124,484'
    """
    value_string = str(value) if not isinstance(value, list) else ','.join(map(str, value))
    return '='.join([key, value_string])


def dict_to_string(parameters):
    """
    input: dictionary of parameters
    output: string 'key1=value1&key2=value2&...'
    """
    return '&'.join(dict_item_to_string(key, value) for key, value in parameters.items())