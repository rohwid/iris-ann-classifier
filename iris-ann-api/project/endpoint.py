import os
import joblib
import yaml

import numpy as np

from keras.models import load_model
from sklearn.preprocessing import normalize
from flask import Flask, request
from flask_restful import Api, Resource


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

f = open("params/classifier.yml", "r")
params = yaml.load(f, Loader=yaml.SafeLoader)
f.close()

model = load_model(params['MODEL'])

app = Flask(__name__)
api = Api(app)

class Classifier(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)

            x = np.NaN

            if len(json_data) > 1:
                for i, data in enumerate(json_data):
                    if i == 0:
                        x = np.array([[data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']]])
                    else:
                        x_data = np.array([[data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']]])
                        x = np.concatenate([x, x_data])
            else:
                x = np.array([[json_data['sepal_length'], json_data['sepal_width'], json_data['petal_length'], json_data['petal_width']]])

            X = joblib.load(params['DUMPED_DATA'])

            X = normalize(np.concatenate([X, x]), axis=1)
            X = np.array(X[(0 - len(json_data)):, :])

            prediction = model.predict(X)

            predict_label = np.argmax(prediction, axis = 1)

            return {
                'response': predict_label.tolist()
            }, 200
        except Exception as err:
            return {
                'message': err
            }, 500

api.add_resource(Classifier, '/predict')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True, port = '5000')
