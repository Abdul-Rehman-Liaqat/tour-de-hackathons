#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 15:57:57 2018

@author: abdulliaqat
"""
    
        # /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()
    
    # Add a message
    resp.message("demo 2 for humanitarian hackathon ICLA")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    
'''    
from twilio.rest import Client
# put your own credentials here
account_sid = "ACa55a95ee55c5b213f6b6430df33fa845"
auth_token = "576888fcc67b7059b5d0b2ad1a5d0199"
client = Client(account_sid, auth_token)
client.messages.create(
  to="+4917658674524",
  from_="+33644603688 ",
      body="Select one option: 1- Medical 2- Legal 3- Food")
'''
'''
from twilio.rest import Client

account_sid = "ACa55a95ee55c5b213f6b6430df33fa845"
auth_token = "576888fcc67b7059b5d0b2ad1a5d0199"
client = Client(account_sid, auth_token)

for sms in client.messages.list():
    print(sms.to)
'''