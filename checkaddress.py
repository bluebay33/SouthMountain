# coding=utf-8
#---------------------------------------------------------------------
# Name : Address Checker
# Propers: check if address of company is valid
# By : Bluebay
# Date: Jan 25, 2022
# Method: 
#     read data from address.cvs, check each address with website USPS.COM, 
#     get the result and write it in result.csv
#---------------------------------------------------------------------


import json
import requests
import pandas as pd

def checkAddr(row):
    url ='https://tools.usps.com/tools/app/ziplookup/zipByAddress'
    payload = {'companyName': row['Company'],
               'address1': row['Street'],
               'city': row['City'],
               'state': row['St'],
               'zip': row['ZIPCode']
               }
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '127',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://tools.usps.com',
        'referer': 'https://tools.usps.com/zip-code-lookup.htm?byaddress',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    response = requests.request("POST",url, headers=headers, data=payload, timeout=200)
    res = response.content.decode()
    return json.loads(res, strict=False)

if __name__ == '__main__':

    df = pd.read_csv('address.csv', header=0)
    if len(df)>0:
        for i, row in df.iterrows():
            print(i+1,' ', list(row), end=' ')
            r = checkAddr(row)
            if r['resultStatus']=='SUCCESS':
                df.loc[i, 'Address Status'] = 'Valid'
                print('--- Vaild')
            else:
                df.loc[i, 'Address Status'] = 'Invalid'
                print('--- Invaild')
        df.to_csv('result.csv')
        print('Finish!')
    else:
        print('Cannot read source data!')
    
    
        
