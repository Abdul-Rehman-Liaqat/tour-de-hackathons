# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Fri Aug 24 10:59:04 2018
#
# @author: abdulliaqat
# """

from werkzeug.datastructures import FileStorage
from flask import Flask, request, Response
import json
import numpy as np
import cv2
from PIL import Image
import io
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import json

# Initialize the Flask application
app = Flask(__name__)


model_name = "model.hdf5"
model_meta = "model_meta.json"
model = load_model(model_name)

fruit_life = {
    "oranges": {"shelf": 10, "refrigerator": 15},
    "apples": {"shelf": 18, "refrigerator": 30},
    "banana": {"shelf": 3, "refrigerator": 5},
}


with open(model_meta, "r") as file:
    model_meta = json.load(file)


def load_and_predict_image():
    test_image = image.load_img("predictions/img.png", target_size=(100, 100))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    return model.predict(test_image)


def find_time_to_live(prediction_probability):
    print(prediction_probability)
    probability_mapping = dict(
        zip(list(model_meta.keys()), list(prediction_probability[0]))
    )
    predicted_class = max(probability_mapping, key=probability_mapping.get)
    opposite_condition = list(probability_mapping.keys())[
        abs(3 - (list(probability_mapping.keys()).index(predicted_class)))
    ]
    print(predicted_class, opposite_condition)
    predicted_fruit = [
        fruit for fruit in list(fruit_life.keys()) if fruit in predicted_class
    ][0]
    if "fresh" in predicted_class:
        predicted_class_life = fruit_life[predicted_fruit]
        proportion_life_left = (
            probability_mapping[predicted_class]
            - probability_mapping[opposite_condition]
        ) / probability_mapping[opposite_condition]
        random_life = np.random.uniform(low = 0.7,high = 0.95)
        return {
            "food": predicted_fruit,
            "best_before": {
                "shelf": predicted_class_life["shelf"] * random_life,
                "refrigerator": predicted_class_life["refrigerator"]
                * random_life,
            },
        }
    else:
        return {
            "food": predicted_fruit,
            "best_before": {"shelf": -1, "refrigerator": -1},
        }


# route http posts to this method
@app.route("/api/image", methods=["POST"])
def prediction():
    imagefile = request.files["file"].read()
    npimg = np.fromstring(imagefile, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    cv2.imwrite("predictions/img.png", img)
    print(img.shape)
    prediction_probability = load_and_predict_image()
    time_to_live = find_time_to_live(prediction_probability)
    return Response(
        response=json.dumps(time_to_live), status=200, mimetype="application/json"
    )


# route http posts to this method
@app.route("/api/test", methods=["POST"])
def test():
    return Response(
        response=json.dumps({"food": "apple", "best_before": 124}),
        status=200,
        mimetype="application/json",
    )


# start flask app
app.run(host="0.0.0.0", port=5000, debug=True)
