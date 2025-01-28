import base64
from io import BytesIO

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from PIL import Image

# Load pre-trained models
KNN = joblib.load("models/knn.pkl")
NN = joblib.load("models/nn.pkl")
RANDOM_FOREST = joblib.load("models/random_forest.pkl")
TREE = joblib.load("models/tree.pkl")

# Global variable to handle model selection
MODEL = KNN

# Initialize Flask application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Auto-reload templates for development


# Route to render the main index page
@app.route("/")
def index():
    """
    Renders the main index.html template.
    This is the entry point of the web application.
    """
    return render_template("index.html")

# Route to handle image prediction requests
@app.route("/predict", methods=["POST"])
def predecir():
    """
    Handles the prediction logic for the uploaded image.
    Processes the image, loads the model, and returns the predicted class.
    """
    # Image preprocessing
    data = request.json  # Get JSON data from the request
    base64_img = data["image"].split(",")[1]  # Extract base64 image data
    decoded_img = base64.b64decode(base64_img)  # Decode base64 to binary image data
    original_img = Image.open(BytesIO(decoded_img))  # Open image using PIL
    resized_img = original_img.resize((28, 28))  # Resize image to 28x28 pixels
    np_img = np.array(resized_img)  # Convert image to a NumPy array
    img = np_img[:, :, -1].reshape((1, -1))  # Extract the last channel and flatten

    # Selective image processing: RF and TC models were trained with neither normalized 
    # data nor PCA reduction since best scores were obtained with those data-sets.
    if MODEL in (RANDOM_FOREST, TREE):
        img_final = img.reshape(1, -1)  # Flatten the image
        # Both models were trained using this column name pattern:
        feature_names = [f"pixel{i + 1}" for i in range(784)]  # For 28x28 image
        img_final = pd.DataFrame(img_final, columns=feature_names)

    else:
        img_final = img / 255.0

    # # Debugging: Print normalized image data and its shape
    # print("Normalized Image Data:")
    # print(img_final)
    # print("Image Shape:", img_final.shape)

    # # Debugging: Print selected model
    # print(MODEL)

    # Get prediction from the model
    pred = MODEL.predict(img_final)  # Predict the class of the image

    # Map predicted class index to class name
    class_names = {
        0: "t-shirt/top",
        1: "trouser",
        2: "pullover",
        3: "dress",
        4: "coat",
        5: "sandal",
        6: "shirt",
        7: "sneaker",
        8: "bag",
        9: "ankle boot",
    }

    prediction = class_names[pred[0]]  # Get the class name from the predicted index

    # Debugging: Print the predicted class
    print("Predicted Class:", prediction)

    # Return the predicted class as the response
    return prediction

@app.route("/select-knn", methods=["POST"])
def select_knn():
    global MODEL, KNN
    MODEL = KNN
    return jsonify({"message": "knn model selected"})


@app.route("/select-nn", methods=["POST"])
def select_nn():
    global MODEL, NN
    MODEL = NN
    return jsonify({"message": "nn model selected"})


@app.route("/select-random-forest", methods=["POST"])
def select_random_forest():
    global MODEL, RANDOM_FOREST
    MODEL = RANDOM_FOREST
    return jsonify({"message": "random forest model selected"})


@app.route("/select-tree", methods=["POST"])
def select_tree():
    global MODEL, TREE
    MODEL = TREE
    return jsonify({"message": "tree model selected"})

# # Run the Flask application
# if __name__ == "__main__":
#     app.run(debug=True)  # Start the app in debug mode for development
