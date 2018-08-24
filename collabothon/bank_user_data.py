#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 09:42:40 2018

@author: abdulliaqat
"""

# Use user-data from bank

import requests
import json
from flask import Flask, request, jsonify


keyid = '0067be03-fec8-4735-9742-0b0a5255d083'
accounts_api_url = "https://api-sandbox.commerzbank.com/accounts-api/v1-s/accounts"
customers_api_url = " https://api-sandbox.commerzbank.com/customers-api/v1-s/persons?firstName=Lea"
firstName = 'Marc'


# get user information
def get_user_info(firstName,keyid):    
    url = "https://api-sandbox.commerzbank.com/customers-api/v1-s/persons"    
    querystring = {"firstName":firstName}    
    headers = {'keyid': keyid}    
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)

# get user accounts
def get_user_accounts(person_id,keyid):    
    url = "https://api-sandbox.commerzbank.com/customers-api/v1-s/persons/{}/agreements".format(person_id)    
    headers = {'keyid': keyid}        
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)

# get transaction details for a user
def get_user_trans_data(account_id,keyid):
    url = "https://api-sandbox.commerzbank.com/accounts-api/v1-s/accounts/{}".format(account_id)    
    headers = {'keyid': keyid}        
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)
    

def get_response(url,keyid):
    headers = {
        'keyid': keyid}
    response = requests.request("GET", url, headers=headers)    
    return json.loads(response.text)
    


app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def create_account():
 #   keyid = request.headers.get('keyid')
    keyid = '0067be03-fec8-4735-9742-0b0a5255d083'
    headers = {
        'content-type': 'application/json',
        'keyid': keyid}
    #account_id = str(28447991)
    data = '{\n"accountId": \"11111126\",\
            \n"currency": "euro",\
            \n"iban": "DE123344",\
            \n"accountType": "secondary",\
            \n"balances": [\n{\n"closingBooked": {\n"amount": {\n"currency": "euro",\
            \n"amount": 1000.00\n},\
            \n"date": "2018-08-24",\
            \n"lastActionDateTime": "2018-08-24"\n}\n}\n]\n}'
    account_id = data.split('accountId')[1].split(':')[1].split(',')[0].split('\"')[1]
    response = requests.post('https://api-sandbox.commerzbank.com/accounts-api/v1-s/accounts/{}'.format(account_id), headers=headers, data=data)    
    if(response.text == 'Created'):
        data = get_user_trans_data(int(account_id),keyid)
 #   print(data)
    return (jsonify(data))


    
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=2222,debug=True)



#user_info = get_user_info(firstName,keyid) 
#user_account = get_user_accounts(int(user_info[0]['personId']),keyid)['agreements'][0]['accountId']
#user_trans_his = get_user_trans_data(user_account,keyid)
#text,account_id  = create_account(keyid)
#if(text == 'Created'):
#    data = get_user_trans_data(account_id,keyid)
#print(data)
# resposne.text to json or dictionary