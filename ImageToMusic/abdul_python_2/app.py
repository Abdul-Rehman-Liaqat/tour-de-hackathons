
from flask import Flask,render_template, url_for, request,redirect
import requests
import numpy as np
import pandas as pd
from subprocess import call

app = Flask(__name__)
#@app.route("/")
#def main():
#    return render_template('send_url.html')

@app.route('/')
def sendData():
    # here we want to get the value of user (i.e. ?url=some-value)
    url_address = request.get_json() 
    print(url_address)
    

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=2222,debug=True)
      