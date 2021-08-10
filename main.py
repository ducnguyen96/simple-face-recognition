from src.extractor import get_all_embedding, prepare_data
from src.classification import classify, train_classification_model
# from sklearn.preprocessing import LabelEncoder
# import numpy as np
# import cv2 as cv
# # from src.extractor import extract_face
# import joblib
# from keras.models import load_model

# from flask import Flask, request, render_template


# # load train dataset
# data = np.load(
#     './src/model/data/5-celebrity-faces-dataset.npz', allow_pickle=True)
# trainy = data['arr_1']

# out_encoder = LabelEncoder()
# out_encoder.fit(trainy)

# facenet_model = load_model('./src/model/keras/facenet_keras.h5')
# facenet_model._make_predict_function()
# classification_model = joblib.load('./src/model/data/my_model.pkl')

# app = Flask(__name__, template_folder='./src/templates')


# @app.route('/', methods=['GET'])
# def home():
#     return render_template('home/index.html')


# # @app.route('/who-is-this', methods=['POST'])
# # def test():
# #     img = cv.imdecode(np.fromstring(
# #         request.files['img'].read(), np.uint8), cv.IMREAD_UNCHANGED)
# #     _, anchor = extract_face(img)
# #     return {
# #         "anchor": list(map(int, anchor))
# #     }

# @app.route('/who-is-this', methods=['POST'])
# def predict():
#     img = cv.imdecode(np.fromstring(
#         request.files['img'].read(), np.uint8), cv.IMREAD_UNCHANGED)

#     return classify(img, out_encoder, facenet_model, classification_model)


if __name__ == "__main__":
    # app.run(host='0.0.0.0')

    prepare_data()

    get_all_embedding()

    train_classification_model()
