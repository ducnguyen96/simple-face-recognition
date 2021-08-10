import joblib
from keras.models import load_model

global facenet_model
global classification_model

facenet_model = load_model('./src/model/keras/facenet_keras.h5')
classification_model = joblib.load('./src/model/data/my_model.pkl')
