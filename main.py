from src.classification import classify
from sklearn.preprocessing import LabelEncoder
import numpy as np
import cv2 as cv
import joblib
from keras.models import load_model
import pickle

from flask import Flask, request, render_template
# from flask_cors import CORS


# load train dataset
trainy = np.array([])
with open('./src/model/data/trainy', 'rb') as fp:
    itemlist = pickle.load(fp)
    trainy = np.array(itemlist)

out_encoder = LabelEncoder()
out_encoder.fit(trainy)

facenet_model = load_model('./src/model/keras/facenet_keras.h5')
facenet_model._make_predict_function()
classification_model = joblib.load('./src/model/data/my_model.pkl')

app = Flask(__name__, template_folder='./src/templates')
# CORS(app, origins=['localhost', 'wikipedia'])


@app.route('/', methods=['GET'])
def home():
    return render_template('home/index.html')


@app.route('/who-is-this', methods=['POST'])
def predict():
    img = cv.imdecode(np.fromstring(
        request.files['img'].read(), np.uint8), cv.IMREAD_COLOR)

    return classify(img, out_encoder, facenet_model, classification_model)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
