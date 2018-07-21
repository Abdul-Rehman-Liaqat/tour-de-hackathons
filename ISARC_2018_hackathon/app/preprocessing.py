#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 10:30:28 2018

@author: abdulliaqat
"""

import requests
import panadas as pd
import numpy as np



content=[]
lat_long_list = [[40.850247,-73.895282],
[40.959615	,-73.80861],
[40.811097	,-73.878641],
[40.802965	,-73.90999],
[40.82747	,-73.843684],
[40.656612	,-73.879323],
[40.680747	,-73.983364],
[40.724589	,-73.939937],
[40.703098	,-73.969617],
[40.703188	,-73.78754],
[40.641238	,-73.778021]]

for location in lat_long_list:
    content.append([])
    for i in range(1,20):
        start_date = '2018-07-{}T00:00:00'.format(i) 
        end_date = '2018-07-{}T00:00:00'.format(i+1) 
        req_variable = r"https://api.breezometer.com/baqi/?end_datetime={}&interval=1&key=de4fef0f7fb349f29f3f21c275018069&lang=en&lat={}&lon={}&start_datetime={}".format(end_date,location[0],location[1],start_date)
        content[-1].append(requests.get(req_variable).json())
        print(len(content[-1][-1]))
"https://api.breezometer.com/baqi/?end_datetime={}&interval=1&key=de4fef0f7fb349f29f3f21c275018069&lang=en&lat={}&lon={}&start_datetime={}".format(end_date,location[0],location[1],start_date)
"https://api.breezometer.com/baqi/?lat=40.7324296&lon=-73.9977264&interval=1&start_datetime=2018-07-01T00:00:00&end_datetime=2018-07-02T00:00:00&key=e7531d2d67894bd7a2c6eaf7f950c374"
"https://api.breezometer.com/baqi/?end_datetime=2018-07-02T00:00:00&interval=1&key=de4fef0f7fb349f29f3f21c275018069&lang=en&lat=40.7324296&lon=-73.9977264&start_datetime=2018-07-01T00:00:00"
start_date = '2018-07-20T00:00:00'
end_date = '2018-07-02T00:00:00'
#req = r"https://api.breezometer.com/baqi/?lat=40.7324296&lon=-73.9977264&interval=1&start_datetime=2018-07-10T00:00:00&end_datetime=2018-07-11T05:25:00&key=e7531d2d67894bd7a2c6eaf7f950c374"
req_variable = r"https://api.breezometer.com/baqi/?lat=40.7324296&lon=-73.9977264&interval=1&datetime={}&key=e7531d2d67894bd7a2c6eaf7f950c374".format(start_date)
req_hack = r"https://api.breezometer.com/baqi/?end_datetime={}&interval=1&key=de4fef0f7fb349f29f3f21c275018069&lang=en&lat={}&lon={}&start_datetime={}".format(end_date,location[0],location[1],start_date)
content = requests.get(req_hack)


pollution_data_columns = ['datetime','lat','long','co','no2','o3','pm10','pm25','so2']
pollution_data = pd.DataFrame(columns=pollution_data_columns)


for location,con in zip(lat_long_list,content):
        for i,data in zip(range(1,20),con):
            start_date = '2018-07-{}T00:00:00'.format(i) 
            end_date = '2018-07-{}T00:00:00'.format(i+1)
            for hour_data in data:
                datetime = hour_data['datetime']
                lat = location[0]
                long = location[1]
                co = hour_data['pollutants']['co']['concentration']
                no2 = hour_data['pollutants']['no2']['concentration']
                o3 = hour_data['pollutants']['o3']['concentration']
                pm10 = hour_data['pollutants']['pm10']['concentration']
                pm25 = hour_data['pollutants']['pm25']['concentration']
                so2 = hour_data['pollutants']['so2']['concentration']
                pollution_data.loc[len(pollution_data)] = [datetime,lat,long,co,no2,o3,pm10,pm25,so2]           
                
pollution_data.to_csv('pollution_data1.csv',index = False)