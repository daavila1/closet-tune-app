import base64
from io import BytesIO

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from PIL import Image

# Load pre-trained machine learning models
KNN = joblib.load("models/knn.pkl")  # K-Nearest Neighbors model
NN = joblib.load("models/nn.pkl")  # Neural Network model
RANDOM_FOREST = joblib.load("models/random_forest.pkl")  # Random Forest model
TREE = joblib.load("models/tree.pkl")  # Decision Tree model

# Global variable to handle the currently selected model
MODEL = KNN  # Default model is KNN

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

    Steps:
    1. Decode the base64 image data from the request.
    2. Preprocess the image (resize, convert to grayscale, invert, etc.).
    3. Prepare the image data for the selected model.
    4. Use the model to predict the class of the image.
    5. Map the predicted class index to a human-readable label.
    6. Return the predicted class as the response.
    """
    # Image preprocessing
    data = request.json  # Get JSON data from the request
    base64_img = data["image"].split(",")[1]  # Extract base64 image data
    img_source = data.get("source", "unknown")  # Extract source data
    decoded_img = base64.b64decode(base64_img)  # Decode base64 to binary image data

    # Debugging:
    # print(img_source)
    
    # If image source is canvas (drawing)
    if img_source == "canvas":
        original_img = Image.open(BytesIO(decoded_img))  # Open image using PIL
        resized_img = original_img.resize((28, 28))  # Resize image to 28x28 pixels
        np_img = np.array(resized_img)  # Convert image to a NumPy array
        img = np_img[:, :, -1].reshape((1, -1))  # Extract the last channel and flatten

    # Else image was uploaded by user
    else:
        # Open the image and convert to grayscale
        original_img = Image.open(BytesIO(decoded_img)).convert("L")
        resized_img = original_img.resize((28, 28))  # Resize to 28x28 pixels
        np_img = np.array(resized_img)  # Convert to NumPy array (2D: height × width)

        # Invert pixel values (0 -> 255, 255 -> 0)
        np_img = 255 - np_img  # Invert to match dataset format

        # Flatten the 2D array into a 1D array
        img = np_img.reshape((1, -1))  # Reshape to (1, 784)

    # Selective image processing: RF and TC models were trained with neither normalized
    # data nor PCA reduction since best scores were obtained with those data-sets.
    if MODEL in (RANDOM_FOREST, TREE):
        # Random Forest and Decision Tree models were trained without normalization or PCA
        img_final = img.reshape(1, -1)  # Flatten the image
        # Create feature names for the DataFrame (pixel1, pixel2, ..., pixel784)
        feature_names = [f"pixel{i + 1}" for i in range(784)]
        img_final = pd.DataFrame(img_final, columns=feature_names)
    else:
        # Normalize image data for KNN and Neural Network models
        img_final = img / 255.0

    # # Debugging: Print normalized image data and its shape
    # print(img)
    # print("Image Shape:", img_final.shape)

    # Debugging: Print the selected model
    # print("Selected Model:", MODEL)

    # If canvas is empty, trigger message
    if np.all(img == 0) or np.all(img == 255):
        prediction = "Canvas is empty, draw or upload and image."

    # Else send image to the model
    else:
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
        # print("Predicted Class:", prediction)

    # Return the predicted class as the response
    return prediction


# Route to select the KNN model
@app.route("/select-knn", methods=["POST"])
def select_knn():
    """
    Sets the global MODEL variable to the KNN model.
    """
    global MODEL, KNN
    MODEL = KNN
    return jsonify({"message": "KNN model selected"})


# Route to select the Neural Network model
@app.route("/select-nn", methods=["POST"])
def select_nn():
    """
    Sets the global MODEL variable to the Neural Network model.
    """
    global MODEL, NN
    MODEL = NN
    return jsonify({"message": "Neural Network model selected"})


# Route to select the Random Forest model
@app.route("/select-random-forest", methods=["POST"])
def select_random_forest():
    """
    Sets the global MODEL variable to the Random Forest model.
    """
    global MODEL, RANDOM_FOREST
    MODEL = RANDOM_FOREST
    return jsonify({"message": "Random Forest model selected"})


# Route to select the Decision Tree model
@app.route("/select-tree", methods=["POST"])
def select_tree():
    """
    Sets the global MODEL variable to the Decision Tree model.
    """
    global MODEL, TREE
    MODEL = TREE
    return jsonify({"message": "Decision Tree model selected"})
