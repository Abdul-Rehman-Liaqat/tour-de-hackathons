#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 09:42:40 2018

@author: abdulliaqat
"""

# Use user-data from bank

import requests
import json
accounts_api_url = "https://api-sandbox.commerzbank.com/accounts-api/v1-s/accounts"
customers_api_url = "https://api-sandbox.commerzbank.com/accounts-api/v1-s/accounts"



headers = {
    'keyid': "0067be03-fec8-4735-9742-0b0a5255d083"}

accounts_api_response = requests.request("GET", accounts_api_url, headers=headers)
accounts_api_response = requests.request("GET", accounts_api_url, headers=headers)
data = json.loads(response.text)


def get_response(url,keyid):
    headers = {
        'keyid': keyid}
    response = request.request("GET", url, headers=headers)
    return json.loads(response.text)
    

# resposne.text to json or dictionary