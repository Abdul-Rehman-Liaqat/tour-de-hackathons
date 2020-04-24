#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 16:49:33 2019

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

path = "/home/abdulliaqat/lovefoodhackwaste/backend/data/fruits-fresh-and-rotten-for-classification/dataset"

model = Sequential()
model.add(Conv2D(32, (3, 3), activation="sigmoid", input_shape=(100, 100, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(256, activation="sigmoid"))
model.add(Dropout(0.5))
model.add(Dense(6, activation="softmax"))
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.summary()


datagen = ImageDataGenerator()
training_generator = datagen.flow_from_directory(
    os.path.join(path, "raw_train"),
    target_size=(100, 100),
    batch_size=4,
    class_mode="categorical",
)

test_generator = datagen.flow_from_directory(
    os.path.join(path, "raw_test"),
    target_size=(100, 100),
    batch_size=4,
    class_mode="categorical",
)

model.fit_generator(
    training_generator,
    steps_per_epoch=63,
    epochs=10,
    validation_data=test_generator,
    validation_steps=50,
)

model_name = "model.h5"

model.save(model_name)
model = load_model(model_name)
with open("model_meta.json", "w") as file:
    dump(training_generator.class_indices, file)

test_image = image.load_img(
    path
    + "/test/rottenbanana/rotated_by_15_Screen Shot 2018-06-12 at 8.58.13 PM"
    + ".png",
    target_size=(100, 100),
)
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
result = model.predict(test_image)
result
