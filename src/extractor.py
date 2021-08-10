import numpy as np
import cv2 as cv
import os
from keras.models import load_model


def extract_face(img):

    # Read image from your local file system
    # original_image = cv.imread(img)

    # Convert color image to grayscale for Viola-Jones
    grayscale_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Load the classifier and create a cascade object for face detection
    face_cascade = cv.CascadeClassifier(
        cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

    detected_faces = face_cascade.detectMultiScale(grayscale_image)

    if len(detected_faces) == 0:
        return None, None

    (column, row, width, height) = detected_faces[0]
    # cv.rectangle(
    #     original_image,
    #     (column, row),
    #     (column + width, row + height),
    #     (0, 255, 0),
    #     2
    # )
    face = img[row:row+height, column:column+width]
    # cv.imshow('Image', original_image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    resized = cv.resize(face, (160, 160), interpolation=cv.INTER_AREA)
    return resized, detected_faces[0]


def load_face(dir):
    faces = list()
    # enumerate files
    for filename in os.listdir(dir):
        path = dir + filename
        read_image = cv.imread(path)
        face, _ = extract_face(read_image)
        if face is not None:
            faces.append(face)
    return faces


def load_dataset(dir):
    # list for faces and labels
    X, y = list(), list()
    for subdir in os.listdir(dir):
        path = dir + subdir + '/'
        faces = load_face(path)
        labels = [subdir for i in range(len(faces))]
        print("loaded %d sample for class: %s" %
              (len(faces), subdir))  # print progress
        X.extend(faces)
        y.extend(labels)
    return np.asarray(X), np.asarray(y)


def prepare_model():
    facenet_model = load_model('./src/model/keras/facenet_keras.h5')
    print('Loaded Model')
    return facenet_model


def prepare_data():
    # load train dataset
    trainX, trainy = load_dataset('./data/train/')
    print(trainX.shape, trainy.shape)

    # load test dataset
    testX, testy = load_dataset('./data/val/')
    print(testX.shape, testy.shape)

    # save and compress the dataset for further use
    np.savez_compressed('./src/model/data/5-celebrity-faces-dataset.npz',
                        trainX, trainy, testX, testy)


def get_embedding(model, face):
    # scale pixel values
    face = face.astype('float32')
    # standardization
    mean, std = face.mean(), face.std()
    face = (face-mean)/std
    # transfer face into one sample (3 dimension to 4 dimension)
    sample = np.expand_dims(face, axis=0)
    # make prediction to get embedding
    yhat = model.predict(sample)
    return yhat[0]


def get_all_embedding():
    # load the face dataset
    data = np.load(
        './src/model/data/5-celebrity-faces-dataset.npz', allow_pickle=True)
    trainX, trainy, testX, testy = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']
    print('Loaded: ', trainX.shape, trainy.shape, testX.shape, testy.shape)

    # load model
    facenet_model = prepare_model()

    # convert each face in the train set into embedding
    emdTrainX = list()
    for face in trainX:
        emd = get_embedding(facenet_model, face)
        emdTrainX.append(emd)

    emdTrainX = np.asarray(emdTrainX)
    print(emdTrainX.shape)

    # convert each face in the test set into embedding
    emdTestX = list()
    for face in testX:
        emd = get_embedding(facenet_model, face)
        emdTestX.append(emd)
    emdTestX = np.asarray(emdTestX)
    print(emdTestX.shape)

    # save arrays to one file in compressed format
    np.savez_compressed('./src/model/data/5-celebrity-faces-embeddings.npz',
                        emdTrainX, trainy, emdTestX, testy)
