#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 17:10:53 2018

@author: abdulliaqat
"""

from mongoengine import connect
connect('icla_db',host='localhost',port=27017)

from flask import Flask,render_template, url_for, request,redirect
from flask_mongoengine import MongoEngine

app = Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html')
    
@app.route('/legal/')
def legal():
    return render_template('legal.html')

@app.route('/send_sms/')
def send_sms():
    return render_template('send_sms.html')

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=1234,debug=True)
      