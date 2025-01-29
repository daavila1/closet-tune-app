// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function () {
  // Get the canvas element and its 2D rendering context
  const mainCanvas = document.getElementById('main-canvas');
  const context = mainCanvas.getContext('2d');

  // Set green color in selected model button
  // Get all buttons within the button container 
  const buttons = document.querySelectorAll('.button-container-1 .button');

  // Add click event listener to each button
  buttons.forEach((button) => {
    button.addEventListener('click', function () {
      // Remove "active" class from all buttons
      buttons.forEach((btn) => btn.classList.remove('active'));
      // Add "active" class to the clicked button
      button.classList.add('active');
    });
  });

  // Variables to store the initial coordinates of the drawing
  let initialX;
  let initialY;

  // Function to draw on the canvas
  const draw = (cursorX, cursorY) => {
    context.beginPath(); // Start a new drawing path
    context.moveTo(initialX, initialY); // Move to the initial coordinates
    context.lineWidth = 30; // Set the line width
    context.strokeStyle = '#000'; // Set the line color to black
    context.lineCap = 'round'; // Set the line cap style to round
    context.lineJoin = 'round'; // Set the line join style to round
    context.lineTo(cursorX, cursorY); // Draw a line to the new coordinates
    context.stroke(); // Render the line

    // Update the initial coordinates to the current cursor position
    initialX = cursorX;
    initialY = cursorY;
  };

  // Function to handle mouse down event
  const mouseDown = (evt) => {
    // Get the initial coordinates of the mouse click
    initialX = evt.offsetX;
    initialY = evt.offsetY;
    // Start drawing at the initial coordinates
    draw(initialX, initialY);
    // Add event listener for mouse movement
    mainCanvas.addEventListener('mousemove', mouseMoving);
  };

  // Function to handle mouse movement
  const mouseMoving = (evt) => {
    // Draw a line to the current cursor position
    draw(evt.offsetX, evt.offsetY);
  };

  // Function to handle mouse up event
  const mouseUp = () => {
    // Stop drawing by removing the mouse movement event listener
    mainCanvas.removeEventListener('mousemove', mouseMoving);
  };

  // Add event listeners for mouse down and mouse up events
  mainCanvas.addEventListener('mousedown', mouseDown);
  mainCanvas.addEventListener('mouseup', mouseUp);

  // Get the clear button element
  const clearButton = document.getElementById('clear-button');

  // Add event listener for the clear button
  clearButton.addEventListener('click', function () {
    // Clear the entire canvas
    context.clearRect(0, 0, mainCanvas.width, mainCanvas.height);
    // Clear the prediction text
    const valuePredictionElement = document.getElementById('prediction-value');
    valuePredictionElement.textContent = '';
  });

  // Get the predict button element
  const predictButton = document.getElementById('predict-button');

  // Add event listener for the predict button
  predictButton.addEventListener('click', function () {
    // Convert the canvas content to a base64-encoded image (PNG format)
    const imageBase64 = mainCanvas.toDataURL('image/png');
    // Log the base64 image data to the console (for debugging)
    console.log('Base64 Image Data:', imageBase64);
  });

  // Add event listeners for the select model button
  // Get the buttons
  const knnButton = document.getElementById('knn-button');
  const nnButton = document.getElementById('nn-button');
  const randForestButton = document.getElementById('rand-forest-button');
  const treeButton = document.getElementById('tree-button');

  // Set the KNN button as active by default
  knnButton.classList.add('active');

  knnButton.addEventListener('click', function () {
    axios.post('select-knn')
      .then(function (response) {
        console.log(response.data.message);
      })
  });

  nnButton.addEventListener('click', function () {
    axios.post('/select-nn')
      .then(function (response) {
        console.log(response.data.message);
      })
  });

  randForestButton.addEventListener('click', function () {
    axios.post('/select-random-forest')
      .then(function (response) {
        console.log(response.data.message);
      })
  });

  treeButton.addEventListener('click', function () {
    axios.post('/select-tree')
      .then(function (response) {
        console.log(response.data.message);
      })
  });

  // Get the file input and upload button elements
  const uploadInput = document.getElementById('upload-input');
  const uploadButton = document.getElementById('upload-button');

  // Trigger the file input when the upload button is clicked
  uploadButton.addEventListener('click', function () {
    uploadInput.click(); // Open the file dialog
  });

  // Handle file selection
  uploadInput.addEventListener('change', function (event) {
    const file = event.target.files[0]; // Get the selected file
    if (file) {
      const reader = new FileReader(); // Create a FileReader to read the file

      // When the file is loaded, draw it on the canvas
      reader.onload = function (e) {
        const img = new Image(); // Create an image element
        img.src = e.target.result; // Set the image source to the file data

        // When the image is loaded, draw it on the canvas
        img.onload = function () {
          // Clear the canvas
          context.clearRect(0, 0, mainCanvas.width, mainCanvas.height);

          // Draw the image on the canvas, scaled to fit
          const scale = Math.min(
            mainCanvas.width / img.width,
            mainCanvas.height / img.height
          );
          const width = img.width * scale;
          const height = img.height * scale;
          const x = (mainCanvas.width - width) / 2;
          const y = (mainCanvas.height - height) / 2;

          context.drawImage(img, x, y, width, height);
        };
      };

      reader.readAsDataURL(file); // Read the file as a data URL
    }
  });
});


let wasImageUploaded = false; // Por defecto, asumimos que el usuario dibujará en el canvas
// Modificar el evento de carga de imagen
document.getElementById('upload-input').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        wasImageUploaded = true; // Indicar que la imagen proviene de una subida
    }
});

// Modificar los eventos de dibujo en el canvas
document.getElementById('main-canvas').addEventListener('mousedown', function () {
    wasImageUploaded = false; // Si el usuario empieza a dibujar, la imagen es del canvas
});