#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 18:28:11 2018

@author: abdulliaqat
"""


import requests
import numpy as np
import pandas as pd
from subprocess import call

img_url = "/home/abdulliaqat/Desktop/ImageToMusic/abdul_python/meWhenIamHappy.jpeg"
img_url_2 = "https://grainemediationblog.files.wordpress.com/2013/11/group-of-happy-people-2.jpg?w=300&h=200"
img_url_3 = "https://www.istockphoto.com/de/foto/emp%C3%B6rt-business-personen-gm157480265-9351815"
img_url_4 = "https://media.istockphoto.com/photos/outraged-business-people-picture-id157480265"
img_url_nagl = "https://pbs.twimg.com/profile_images/378800000797221124/5c8cca32852789659fad9003215097c7_400x400.jpeg"
img_url_burak = "http://robotics.ozyegin.edu.tr/wp-content/uploads/2013/12/burak.jpg"
key_path = "subscription_key.txt"
face_api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/detect'


# Get Image

# Get microsoft response and decode
def get_azure_res(face_api_url,key_path,image_url=None,image_path=None):
    f = open(key_path, "r")
    subscription_key = f.readline().strip("\n")
    f.close()
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'emotion'
    }
        #    params = {
    #        'returnFaceId': 'true',
    #        'returnFaceLandmarks': 'false',
    #        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    #    }   

    if(image_url == None and image_path != None):
        headers = { 'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': subscription_key }      
        data = open(image_path, 'rb')
        response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
    if(image_path == None and image_url != None):
        headers = { 'Ocp-Apim-Subscription-Key': subscription_key }        
        response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
    faces = response.json()
    return(faces)

# Select relevant emotions, Average and normalize them
def decode_emotions(res_faces):
    emotions = np.array(list(res_faces[0]["faceAttributes"]["emotion"].values()))
    if(len(res_faces) > 1):
        for face_ind in range(1,len(res_faces)):
            emotions += np.array(list(res_faces[0]["faceAttributes"]["emotion"].values()))
    emo = []
    emo.append(emotions[0])
    emo += emotions[3:]
    emo = np.array(emo)
    return emo/sum(emo)
    
res = get_azure_res(face_api_url,key_path,image_url=img_url_burak)
result = decode_emotions(res)   

# measure distance and return top 10 spotify_id # Get songs from spotify using spotify_ids
songs_emo_df = pd.read_csv("transformed_df_normalized.csv")
songs_emo_val = songs_emo_df[songs_emo_df.columns[2:]].values
from sklearn.neighbors import NearestNeighbors
top_n = 6
nbrs = NearestNeighbors(n_neighbors=top_n, algorithm='ball_tree').fit(songs_emo_val)
distances, indices = nbrs.kneighbors([result])
spotify_id = songs_emo_df["spotify_id"].iloc[indices[0]]

# spotify connection and get links
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQBxrV1ukYS2cUCrYoA3L8DOes29Hf2uUJiktTK9FyJkIinD_iFDvM_TApEfKOGO9hU2Ova9cFWNbFNzv3da1_jdoD4A42iPV88wsBoBE2PM4Vmwd7vnw2mvXlbucnUrC5za5eSAmMpc1YC5nJRO0-S4Ll-S7b4',
}

params = (
    ('ids', ",".join(list(spotify_id.values.astype(str)))),
)

response = requests.get('https://api.spotify.com/v1/artists', headers=headers, params=params)
url = response.json()["artists"][2]["external_urls"]["spotify"]
call(["python","-m","webbrowser","-t","{}".format(url)])
    
