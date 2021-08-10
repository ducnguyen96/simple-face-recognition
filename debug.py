import cv2 as cv
import numpy as np
from src.extractor import draw_face


from flask import Flask, request, render_template
app = Flask(__name__, template_folder='./src/templates')


@app.route('/', methods=['GET'])
def home():
    return render_template('home/index.html')


@app.route('/who-is-this', methods=['POST'])
def predict():
    img = cv.imdecode(np.fromstring(
        request.files['img'].read(), np.uint8), cv.IMREAD_COLOR)

    cv.imshow('img', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    draw_face(img)
    return 'success'


if __name__ == "__main__":
    app.run()
