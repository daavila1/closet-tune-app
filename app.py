import base64
from io import BytesIO

import joblib
import numpy as np
from flask import Flask, render_template, request
from PIL import Image

# Initialize Flask application
app = Flask(__name__)
# app.config["TEMPLATES_AUTO_RELOAD"] = True  # Auto-reload templates for development


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
    img = np_img[:, :, -1].reshape(
        (1, -1)
    )  # Extract the last channel and flatten
    img_norm = img / 255.0  # Normalize pixel values to [0, 1]

    # Debugging: Print normalized image data and its shape
    print("Normalized Image Data:")
    print(img_norm)
    print("Image Shape:", img_norm.shape)

    # Load the pre-trained model
    model = joblib.load("models/nn.pkl")  # Load the model from the specified path

    # Get prediction from the model
    pred = model.predict(img_norm)  # Predict the class of the image

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


# # Run the Flask application
# if __name__ == "__main__":
#     app.run(debug=True)  # Start the app in debug mode for development
