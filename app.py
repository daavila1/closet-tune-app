from flask import Flask, render_template, request

import numpy as np
from PIL import Image
from io import BytesIO
import base64
# import sklearn
import joblib


app = Flask(__name__)


# Render index
@app.route("/")
def index():
    return render_template("index.html")


@app.route('/predecir', methods=['POST'])
def predecir():
    # Image preprocessing
    data = request.json
    base64_img = data['imagen'].split(",")[1]
    decoded_img = base64.b64decode(base64_img)
    original_img = Image.open(BytesIO(decoded_img))
    resized_img = original_img.resize((28, 28))
    np_img = np.array(resized_img)
    img = np_img[:, :, -1].reshape((1, -1))
    img_norm = img / 255.0

    # Test
    print(img_norm)
    print(img_norm.shape)

    # Load model
    model = joblib.load('models/nn.pkl')

    # Get prediction
    pred = model.predict(img_norm)

    # Get class name
    class_names = {0: 'camiseta/top',
                   1: 'pantalón',
                   2: 'pullover',
                   3: 'vestido',
                   4: 'abrigo',
                   5: 'sandalia',
                   6: 'camisa',
                   7: 'zapato',
                   8: 'bolso/maleta',
                   9: 'botín', }
    
    prediction = class_names[pred[0]]

    # Test
    print(prediction)

    return prediction
