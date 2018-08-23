#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 09:41:37 2018

@author: abdulliaqat
"""


from googletrans import Translator
import pandas as pd
# gini Receipt data
translator = Translator()
translator.translate('안녕하세요.')


import goslate
gs = goslate.Goslate()
print(gs.translate('hello world', 'de'))

#Backwaren, Brot, Kuchen	Krustenbrot
#Molkereiprodukte, Fette	Frischmilch 1,5%
#Molkereiprodukte, Fette	Butter Kerrygold
#Fleisch, Geflügel, Wurst	Hähnchenflügel
#Fleisch, Geflügel, Wurst	Hackfleisch gemischt
#Fisch	Matjesfilet
#Getränke, Spirituosen	Mineralwasser classic
#Obst, Gemüse, Pflanzen	Bananen
#Tiefkühlkost	Bami Goreng
#Kaffee, Tee, Süßwaren, Knabberartikel	Paprikachips



# csv file