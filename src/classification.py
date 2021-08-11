from src.extractor import extract_face, get_embedding
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
import numpy as np
import joblib
import cv2 as cv
import operator


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
    # yhat_class = classification_model.predict(emb_norm)
    yhat_prob = classification_model.predict_proba(emb_norm)

    # top 5
    yhat_prob_array = np.array(yhat_prob[0])
    enumerate_object = enumerate(yhat_prob_array)
    sorted_pairs = sorted(
        enumerate_object, key=operator.itemgetter(1), reverse=True)
    sorted_indices = [index for index, element in sorted_pairs]
    sorted_yhat = [element*100 for index, element in sorted_pairs]
    indices_top5 = sorted_indices[:5]
    prob_top5 = sorted_yhat[:5]

    names_top5 = out_encoder.inverse_transform(indices_top5)

    return {
        "names_top5": list(map(str, names_top5)),
        "prob_top5": list(map(float, prob_top5)),
        "anchor": list(map(int, anchor))}
