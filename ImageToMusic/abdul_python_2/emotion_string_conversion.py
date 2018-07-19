#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 16:20:12 2018

@author: abdulliaqat
"""

import requests
import json
import pandas as pd

auth_headers = {
  'Authorization' : 'Token 6f2cd517a5f57d38e4d11e03db3ea872dcabc0a5'
}

n = 5

galiboo_df = pd.read_csv("/home/abdulliaqat/Desktop/ImageToMusic/abdul_python/galiboo.csv",sep = ";")
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
        
song_emotions = pd.DataFrame(emotion_values,columns=cols[0:18])
song_emotions["galiboo_id"] = list(random_df.track_id)

song_emotions.to_csv("songs_emotions_df.csv",index=False)



general_keys = res.json().keys()
#dict_keys(['_id', 'analysis', 'artists', 'audio_url', 'external_ids', 'success', 'title'])

analysis_keys = res.json()["analysis"].keys()
#dict_keys(['acousticness', 'danceability', 'energy', 'instrumentalness', 'smart_tags', 'tags', 'valence'])

smart_tags_keys = res.json()["analysis"]["smart_tags"].keys()
#dict_keys(['overall_predictions', 'segment_predictions'])

overall_predictions_keys = res.json()["analysis"]["smart_tags"]["overall_predictions"].keys()
overall_predictions_keys = list(overall_predictions_keys)

emotions=[]
for ind,e in overall_predictions_keys:
    emotions.append([])
    temp = ind.split("-")[0]
    
    
emotions = [["Angry","Agressive"],
["Arousing","Awakening"],
["Bizarre","Weird"],
["Calming","Soothing"],
["Carefree","Lighthearted"],
["Cheerful","Festive"],
["Emotional","Passionate"],
["Exciting","Thrilling"],
["Happy"],
["Laid-back","Mellow"],
["Light","Playful"],
["Loving","Romantic"],
["Pleasant","Comfortable"],
["Positive","Optimistic"],
["Powerful","Strong"],
["Sad"],
["Tender","Soft"],
["Touching","Loving"]]



microsoft_emotion = ["anger","contempt","disgust","fear","happiness","neutral","sadness","surprise"]

galiboo_microsoft = {"anger":["Angry","Emotional","Passionate","Agressive"],
                     "happiness":["Happy","Positive","Exciting","Thrilling","Cheerful","Festive","Arousing","Awakening","Loving","Romantic","Optimistic","Touching"],
                     "sadness":["Sad"],
                     "neutral":["Calming","Soothing","Laid-back","Mellow","Light","Playful","Pleasant","Comfortable","Tender","Soft","Carefree","Lighthearted"],
                     "surprise":["Powerful","Strong"]}



galiboo_microsoft_2 = {"anger":["Angry","Emotional"],
                     "happiness":["Happy","Positive","Exciting","Cheerful","Arousing","Loving","Touching"],
                     "sadness":["Sad"],
                     "neutral":["Calming","Laid-back","Light","Pleasant","Tender","Carefree"],
                     "surprise":["Powerful"]}



transformed_df = pd.DataFrame()
transformed_df["anger"] = df[galiboo_microsoft_2["anger"]].apply(max,axis=1)
transformed_df["happiness"] = df[galiboo_microsoft_2["happiness"]].apply(max,axis=1)
transformed_df["sadness"] = df[galiboo_microsoft_2["sadness"]].apply(max,axis=1)
transformed_df["neutral"] = df[galiboo_microsoft_2["neutral"]].apply(max,axis=1)
transformed_df["surprise"] = df[galiboo_microsoft_2["surprise"]].apply(max,axis=1)
transformed_df_normalized = transformed_df.apply(lambda x:x/sum(x),axis=1)
transformed_df_normalized["spotify_id"] = df["spotify_id"]
transformed_df_normalized["galiboo_id"] = df["galiboo_id"]
    transformed_df["spotify_id"] = df["spotify_id"]
    transformed_df["galiboo_id"] = df["galiboo_id"]




vocals=[
"Aggressive",
"Altered_with_Effects",
"Breathy",
"Call_&_Response",
"Duet",
"Emotional",
"Falsetto",
"Gravelly",
"High-pitched",
"Low-pitched",
"Monotone",
"Rapping",
"Screaming",
"Spoken",
"Strong",
"Vocal_Harmonies"
]


segment_predictions_keys = res.json()["analysis"]["smart_tags"]["segment_predictions"].keys()
segment_predictions_keys = list(segment_predictions_keys)
