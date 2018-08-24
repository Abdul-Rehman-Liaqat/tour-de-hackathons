#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 11:44:07 2018

@author: abdulliaqat
"""

import werkzeug
from flask_restplus import reqparse

file_upload = reqparse.RequestParser()
file_upload.add_argument('Receipt_Image',  
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='Please upload receipt image')

