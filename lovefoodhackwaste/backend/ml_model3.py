#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 01:41:54 2019

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
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint

from PIL import Image
from time import time
import numpy as np
from json import dump


base_model = ResNet50(weights='imagenet', include_top=False, input_shape = (100,100,3))


num_classes = 6

x = Flatten()(base_model.output)
x = Dense(4096, activation='relu')(x)
x = Dropout(0.5)(x)
x = BatchNormalization()(x)
predictions = Dense(num_classes, activation = 'softmax')(x)
head_model = Model(input = base_model.input, output = predictions)
head_model.compile(optimizer = 'rmsprop', loss = 'categorical_crossentropy', metrics = ['accuracy'])
checkpointer = ModelCheckpoint(filepath='/content/model.hdf5', verbose=1, save_best_only=True)

head_model.fit_generator(
    training_set,
    steps_per_epoch = 344,
    epochs = 10,
    validation_data=test_set,
    validation_steps = 250,
    callbacks=[checkpointer]
)
