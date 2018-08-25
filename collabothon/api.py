#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 11:43:11 2018

@author: abdulliaqat
"""

from flask import Flask
from flask_restplus import Resource, Api,reqparse
from flask import Flask, request, jsonify
import requests
import json
import werkzeug

import parsers



app = Flask(__name__)
api = Api(app)
@api.route('/upload/')
class my_file_upload(Resource):
    @api.expect(parsers.file_upload)
    def post(self):
        args = parsers.file_upload.parse_args()
        return {'status': 'Done'}
    
    
    
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=9999,debug=True)
