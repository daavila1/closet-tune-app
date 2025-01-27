// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function () {
  // Get the canvas element and its 2D rendering context
  const mainCanvas = document.getElementById('main-canvas');
  const context = mainCanvas.getContext('2d');

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
});
