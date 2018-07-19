#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 22:17:12 2018

@author: abdulliaqat
"""

import requests
import pandas as pd
import os

cwd = os.getcwd()

auth_headers = {
  'Authorization' : 'Token 6f2cd517a5f57d38e4d11e03db3ea872dcabc0a5'
}

n = 15000

galiboo_df = pd.read_csv(cwd+"/galiboo.csv",sep = ";")
galiboo_df.track_id = galiboo_df["track_id"].str.strip()
random_df = galiboo_df.sample(n)

cols= ["Angry","Arousing","Bizarre","Calming","Carefree","Cheerful","Emotional",
"Exciting","Happy","Laid-back","Light","Loving","Pleasant","Positive","Powerful","Sad","Tender","Touching","track_id"]
song_emotions = pd.DataFrame(columns=cols)

response = []
emotion_values = []

for ind in range(len(random_df)):
    track_id = galiboo_df["track_id"].iloc[ind]
    res_temp = requests.get('http://secure.galiboo.com/api/metadata/tracks/' + track_id + '/',
         headers=auth_headers)
    emotion_values.append( list(res_temp.json()["analysis"]["smart_tags"]["overall_predictions"].values())[0:18])
    print(ind)
    if(ind%10==0):
        print("writing csv file")
        song_emotions = pd.DataFrame(emotion_values,columns=cols[0:18])
        song_emotions["galiboo_id"] = list(random_df.track_id[0:ind+1])
        song_emotions["spotify_id"] = list(random_df.spotify_id[0:ind+1])
        song_emotions.to_csv("songs_emotions_df.csv",index=False)
        
        
song_emotions = pd.DataFrame(emotion_values,columns=cols[0:18])
song_emotions["galiboo_id"] = list(random_df.track_id)
song_emotions["spotify_id"] = list(random_df.spotify_id)

song_emotions.to_csv("songs_emotions_df.csv",index=False)