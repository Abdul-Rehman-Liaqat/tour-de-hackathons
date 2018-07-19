#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 17:10:53 2018

@author: abdulliaqat
"""


from flask import Flask,render_template, url_for, request,redirect

app = Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html')
    

@app.route('/submit/', methods=['POST'])
def submit():
#    numbers=["+4917658674524","+4915751034233"]
    numbers=["+4917658674524"]
    account_sid = "ACa55a95ee55c5b213f6b6430df33fa845"
    auth_token = "576888fcc67b7059b5d0b2ad1a5d0199"
    for to_number in numbers:
        client = Client(account_sid, auth_token)
        client.messages.create(
                to=to_number,
                from_="+33644603688 ",
                body=request.form['text'])
    return 'You entered: {}'.format(request.form['text'])

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=1234,debug=True)
      