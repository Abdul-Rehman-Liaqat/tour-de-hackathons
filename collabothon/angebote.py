#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 09:36:06 2018

@author: abdulliaqat
"""

import requests
import json
from flask import Flask, request, jsonify


api_key = 'tUveOAJW'
deal_id = '120035'
# Get angebote data.


# get all deals for location
def location_based_deals(api_key,location):
    url = "https://api.discountapi.com/v2/deals"    
    querystring = {"api_key":api_key,"location":location}        
    response = requests.request("GET", url, params=querystring)
    return json.loads(response.text)

# get  online deals or category specific
def online_deals(api_key,category=False):
    if(category):
        url = "https://api.discountapi.com/v2/deals"    
        querystring = {"api_key":api_key,"online":1,"category_slugs":"electronics"}        
        response = requests.request("GET", url, params=querystring)
        return json.loads(response.text)
    else:   
        url = "https://api.discountapi.com/v2/deals"    
        querystring = {"api_key":api_key,"online":1}        
        response = requests.request("GET", url, params=querystring)
        return json.loads(response.text)

# get one deal
def one_deal(api_key,deal_id):
    url = "https://api.discountapi.com/v2/deals/{}".format(deal_id)    
    response = requests.request("GET", url)
    return json.loads(response.text)


app = Flask(__name__)
@app.route('/getDeal', methods = ['GET', 'POST'])
def getDeal():
    deal_id = '120035'
    url = "https://api.discountapi.com/v2/deals/{}".format(deal_id)    
    response = requests.request("GET", url)
    final_dict = json.loads(response.text)
    data = {}
    data['Name'] = final_dict['deal']['merchant']['name']
    data['Discount'] = final_dict['deal']['discount_amount']
    data['Original_price'] = final_dict['deal']['value']
    data['Discounted_price'] = final_dict['deal']['price']
    return jsonify(data)


    
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=3333,debug=True)
