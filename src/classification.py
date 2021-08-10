from src.extractor import extract_face, get_embedding
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
import numpy as np
import joblib
import cv2 as cv


def train_classification_model():
    # load embedding
    data = np.load(
        './src/model/data/5-celebrity-faces-embeddings.npz', allow_pickle=True)

    emdTrainX, trainy, emdTestX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']

    print("Dataset: train=%d, test=%d" %
          (emdTrainX.shape[0], emdTestX.shape[0]))
    print('emdTrainX shape :', emdTrainX.shape)

    # normalize input vectors
    in_encoder = Normalizer()
    emdTrainX_norm = in_encoder.transform(emdTrainX)
    emdTestX_norm = in_encoder.transform(emdTestX)

    # label encode targets
    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    trainy_enc = out_encoder.transform(trainy)
    testy_enc = out_encoder.transform(testy)

    # fit model
    model = SVC(kernel='linear', probability=True)
    model.fit(emdTrainX_norm, trainy_enc)

    # predict
    yhat_train = model.predict(emdTrainX_norm)
    yhat_test = model.predict(emdTestX_norm)

    # score
    score_train = accuracy_score(trainy_enc, yhat_train)
    score_test = accuracy_score(testy_enc, yhat_test)
    # summarize
    print('Accuracy: train=%.3f, test=%.3f' %
          (score_train*100, score_test*100))

    # save model to disk
    filename = './src/model/data/my_model.pkl'
    joblib.dump(model, filename)


def classify(img, out_encoder, facenet_model, classification_model):
    # detect face
    face, anchor = extract_face(img)

    if face is None:
        return {}

    # get embedding
    emb = get_embedding(facenet_model, face)

    # normalize input
    in_encoder = Normalizer()
    emb_norm = in_encoder.transform([emb])

    # predict
    yhat_class = classification_model.predict(emb_norm)
    yhat_prob = classification_model.predict_proba(emb_norm)

    class_index = yhat_class[0]
    class_probability = yhat_prob[0, class_index] * 100

    print('class_index :', class_index)
    print('class_probability :', class_probability)

    all_names = out_encoder.inverse_transform([0, 1, 2, 3, 4])
    yhat_p0100 = yhat_prob[0]*100
    print('Predicted: \n%s \n%s' % (all_names, yhat_p0100))

    prob_list_of_str = list(map(int, yhat_p0100.tolist()))
    return {"class_index": str(class_index),
            "class_probability": str(class_probability),
            "all_names": all_names.tolist(),
            "all_probability": prob_list_of_str,
            "anchor": list(map(int, anchor))}
