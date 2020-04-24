#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 19:40:21 2019

@author: abdulliaqat
"""


import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from PIL import Image
from time import time
import numpy as np
from json import dump


from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from IPython.display import display
from PIL import Image
import numpy as np
from keras.preprocessing import image


path = "/home/abdulliaqat/lovefoodhackwaste/backend/data/fruits-fresh-and-rotten-for-classification/dataset"

model = Sequential()

model.add(Conv2D(32, (3, 3), activation='sigmoid', input_shape=(100, 100, 3)))
model.add(Conv2D(32, (3, 3), activation='sigmoid'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation='sigmoid'))
model.add(Conv2D(64, (3, 3), activation='sigmoid'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(6, activation='softmax'))
model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
model.summary()



train_datagen = ImageDataGenerator()
training_set = train_datagen.flow_from_directory(
                os.path.join('/content/dataset/','train'),
                target_size = (100,100),
                batch_size = 32,
                class_mode = 'categorical'
    )

test_set = train_datagen.flow_from_directory(
                os.path.join('/content/dataset/','test'),
                target_size = (100,100),
                batch_size = 32,
                class_mode = 'categorical'
    )
model.fit_generator(
    training_set,
    steps_per_epoch = 344,
    epochs = 10,
    validation_data=test_set,
    validation_steps = 250
)


