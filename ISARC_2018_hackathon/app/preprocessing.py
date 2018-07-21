#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 10:30:28 2018

@author: abdulliaqat
"""

import requests
import pandas as pd
import numpy as np
import pickle



content=[]
old_lat_long_list = [[40.850247,-73.895282],
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




lat_long_list = [[40.846951, -73.933641],
 [40.745616, -73.97305],
 [40.7415, -73.95491001],
 [40.817516, -73.80261],
 [40.80218, -73.79324001],
 [40.7727804, -73.83087],
 [40.8006, -73.82895],
 [40.7252805, -74.01128],
 [40.77367, -73.92198],
 [40.7738304, -73.92197],
 [40.730165, -73.87643],
 [40.78647, -73.78812],
 [40.7604, -74.00328],
 [40.76017, -74.00382],
 [40.7604506, -74.003221],
 [40.7605, -74.0032],
 [40.737015, -73.85373001],
 [40.66738, -73.77021],
 [40.66579, -73.75706],
 [40.68314, -73.72692],
 [40.8492, -73.945241],
 [40.7084705, -73.99884],
 [40.70895, -73.996941],
 [40.70158, -73.99033],
 [40.69236, -73.99939],
 [40.76212, -74.91],
 [40.74137, -74.00893],
 [40.73651, -73.975011],
 [40.7601606, -73.95751],
 [40.73868, -73.973391],
 [40.712, -73.97793],
 [40.73895, -74.01012],
 [40.79751, -73.827091],
 [40.67374, -73.80154],
 [40.70538, -74.01528],
 [40.6822, -74.0057201],
 [40.7894, -73.78765],
 [40.79771, -73.92004],
 [40.77391, -73.9222],
 [40.80151, -73.93066],
 [40.8013005, -73.930181],
 [40.793425, -73.79344],
 [40.7889404, -73.789571],
 [40.75605, -73.740851],
 [40.7454306, -73.76907],
 [40.7887906, -73.78895],
 [40.7868604, -73.78838],
 [40.7719, -73.99401],
 [40.66642, -73.78958],
 [40.68361, -73.72646],
 [40.7136604, -73.7292],
 [40.71309, -73.72892],
 [40.74799, -73.73784],
 [40.763521, -73.99935],
 [40.7713004, -73.99455],
 [40.78918, -73.78792],
 [40.77065, -73.834421],
 [40.76191, -73.839121],
 [40.7270705, -73.83231],
 [40.700841, -73.815751],
 [40.7268904, -73.83239],
 [40.7613906, -73.83898],
 [40.7702704, -73.8354],
 [40.77384, -73.92192]]

for location in lat_long_list:
    content.append([])
    for i in range(10,15):
        start_date = '2018-07-{}T00:00:00'.format(i) 
        end_date = '2018-07-{}T00:00:00'.format(i+1) 
        req_variable = r"https://api.breezometer.com/baqi/?end_datetime={}&interval=1&key=de4fef0f7fb349f29f3f21c275018069&lang=en&lat={}&lon={}&start_datetime={}".format(end_date,location[0],location[1],start_date)
        content[-1].append(requests.get(req_variable).json())
        with open('traffic_data_pollution_3.obj','wb') as f:
            pickle.dump(content,f)
        print(len(content[-1][-1]),i,location)

#"https://api.breezometer.com/baqi/?end_datetime={}&interval=1&key=de4fef0f7fb349f29f3f21c275018069&lang=en&lat={}&lon={}&start_datetime={}".format(end_date,location[0],location[1],start_date)
#"https://api.breezometer.com/baqi/?lat=40.7324296&lon=-73.9977264&interval=1&start_datetime=2018-07-01T00:00:00&end_datetime=2018-07-02T00:00:00&key=e7531d2d67894bd7a2c6eaf7f950c374"
#"https://api.breezometer.com/baqi/?end_datetime=2018-07-02T00:00:00&interval=1&key=de4fef0f7fb349f29f3f21c275018069&lang=en&lat=40.7324296&lon=-73.9977264&start_datetime=2018-07-01T00:00:00"
#start_date = '2018-07-20T00:00:00'
#end_date = '2018-07-02T00:00:00'
#req = r"https://api.breezometer.com/baqi/?lat=40.7324296&lon=-73.9977264&interval=1&start_datetime=2018-07-10T00:00:00&end_datetime=2018-07-11T05:25:00&key=e7531d2d67894bd7a2c6eaf7f950c374"
#req_variable = r"https://api.breezometer.com/baqi/?lat=40.7324296&lon=-73.9977264&interval=1&datetime={}&key=e7531d2d67894bd7a2c6eaf7f950c374".format(start_date)
#req_hack = r"https://api.breezometer.com/baqi/?end_datetime={}&interval=1&key=de4fef0f7fb349f29f3f21c275018069&lang=en&lat={}&lon={}&start_datetime={}".format(end_date,location[0],location[1],start_date)
#content = requests.get(req_hack)


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
                
pollution_data.to_csv('pollution_and_traffic_data10_14.csv',index = False)
