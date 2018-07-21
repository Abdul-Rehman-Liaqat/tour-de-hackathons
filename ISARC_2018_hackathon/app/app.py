#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 10:30:28 2018

@author: abdulliaqat
"""

import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from sodapy import Socrata
import requests


df = pd.read_csv('pollution_data1.csv')
m = Basemap(projection='mill',
            llcrnrlat = 40,
            llcrnrlon = -130,
            urcrnrlat = 50,
            urcrnrlon = -60,
            resolution = 'l')
m.drawcoastlines()
m.drawcountries(linewidth=2)
m.drawstates(color='b')
#m.fillcontinents()
#m.bluemarble

nyclat, nyclon = 40.7127, -74.0059
xpt,ypt = m(nyclon,nyclat)
#m.plot(xpt,ypt,'g^',markersize = 25)
m.scatter(xpt, ypt,marker='D',color='m')
plt.title('Basemap tutorial')
plt.show()



client = Socrata("data.cityofnewyork.us", None)
restults = client.get("i4gi-tjb9", where="data_as_of > '2018-07-01T00:00:00.000' and borough in ('Brookly','Manhattan','Queens')",limit='2000000')
results_df = pd.DataFrame.from_records(restults)
results_df['minutes'] = results_df['data_as_of'].apply(lambda x:True if(int(x[14:16])%5 in (1,4,0)) else False)
final_df = results_df[results_df['minutes'] == True]
final_df['data_point'] = final_df['link_points'].apply(lambda x:x.split(' ')[1] if(x.split(' ')[1] != '') else x.split(' ')[2])
points_of_consideration = final_df['data_point'].unique()
points_of_consideration = [[float(i) for i in point.split(',')] for point in points_of_consideration]
#df.datetime = pd.datetime(df.datetime)
#df.index = df.datetime
groups = df.groupby(['lat','long'])
for group in groups.all().index:
    one_group = groups.get_group(group)
    plt.plot(one_group['pm10'])
    plt.plot(one_group['pm25'])
    plt.plot(one_group['co'])
    plt.plot(one_group['o3'])
    plt.plot(one_group['no2'])
    plt.show()
    print(one_group['pm10'].iloc[10])