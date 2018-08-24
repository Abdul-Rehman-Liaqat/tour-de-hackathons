#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 10:59:04 2018

@author: abdulliaqat
"""

from flask import Flask
from flask_restplus import Resource, Api,reqparse
from flask import Flask, request, jsonify
import requests
import json
import werkzeug
import parsers
import time

app = Flask(__name__)
api = Api(app)

# get transaction details for a user
def get_user_trans_data(account_id,keyid):
    url = "https://api-sandbox.commerzbank.com/accounts-api/v1-s/accounts/{}".format(account_id)    
    headers = {'keyid': keyid}        
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)
    


@api.route('/5-Wishlist_Deal')
class GetWishlistDeal(Resource):
    def get(self):
        deal_id = '120035'
        url = "https://api.discountapi.com/v2/deals/{}".format(deal_id)    
        response = requests.request("GET", url)
        final_dict = json.loads(response.text)
        data = {}
        data['1-Name'] = final_dict['deal']['merchant']['name']
        data['4-Discount'] = final_dict['deal']['discount_amount']
        data['2-Original_price'] = final_dict['deal']['value']
        data['3-Discounted_price'] = final_dict['deal']['price']
        return jsonify(data)

@api.route('/1-Create_Account')
class CreateAccount(Resource):
    def get(self):
     #   keyid = request.headers.get('keyid')
        keyid = '0067be03-fec8-4735-9742-0b0a5255d083'
        headers = {
            'content-type': 'application/json',
            'keyid': keyid}
        #account_id = str(28447991)
        data = '{\n"accountId": \"11111130\",\
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
    
@api.route('/2-Decode_Receipt/')
class ParseReceipt(Resource):
    @api.expect(parsers.file_upload)
    def post(self):
        time.sleep(2)
        args = parsers.file_upload.parse_args()
        parsed_dict = {'market':'penny','Date':'18.05.2018','Time':'20:38:56','Items':{'Mango':1.10,
                       'Spargel':2.5,
                       'Hinterschinken':1.49,
                       'Maggi Suppe':0.49,
                       'Choclait Chips':1.19,
                       'PFAND':2.0}}
        return parsed_dict
    
@api.route('/3-Grocery_Deals')
class RecommendGroceryDeals(Resource):
    def get(self):
        time.sleep(2)
        data = {}
        all_item = {}
        data['1-Market'] = 'Kaufland Berlin-Tempelhof'
        data['Product'] = 'Hinterschinken'
        data['2-Actual_price'] = '1.49'
        data['4-Discount'] = '0.74'
        data['3-Discounted_price'] = '0.74'
        all_item[data['Product']] = data
        data = {}
        data['1-Market'] = 'Kaufland Berlin-Tempelhof'
        data['Product'] = 'Eier'
        data['2-Actual_price'] = '1.09'
        data['4-Discount'] = '0.10'
        data['3-Discounted_price'] = '0.94'
        all_item[data['Product']] = data
        return jsonify(all_item)
    
@api.route('/4-Wish_List')
class GetWishlist(Resource):
    def get(self):
        time.sleep(2)
        data = {}
        data['1-Item'] = 'Samsung Galaxy S6/S6 edge'
        data['2-Original_price'] = 599.99
        data['3-Funds_so_far'] = 34.40
        return jsonify(data)
        
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)
#    app.run(debug=True)
