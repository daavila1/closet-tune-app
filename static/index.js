document.addEventListener('DOMContentLoaded', function() {
  const mainCanvas = document.getElementById("main-canvas");
  const context = mainCanvas.getContext("2d");

  let initialX;
  let initialY;

  const dibujar = (cursorX, cursorY) => {
    context.beginPath();
    context.moveTo(initialX, initialY);
    context.lineWidth = 30;
    context.strokeStyle = "#000";
    context.lineCap = "round";
    context.lineJoin = "round";
    context.lineTo(cursorX, cursorY);
    context.stroke();

    initialX = cursorX;
    initialY = cursorY;
  };

  const mouseDown = (evt) => {
    initialX = evt.offsetX;
    initialY = evt.offsetY;
    dibujar(initialX, initialY);
    mainCanvas.addEventListener("mousemove", mouseMoving);
  };

  const mouseMoving = (evt) => {
    dibujar(evt.offsetX, evt.offsetY);
  };

  const mouseUp = () => {
    mainCanvas.removeEventListener("mousemove", mouseMoving);
  };

  mainCanvas.addEventListener("mousedown", mouseDown);
  mainCanvas.addEventListener("mouseup", mouseUp);

  const limpiarButton = document.getElementById('clean-button');

  limpiarButton.addEventListener('click', function() {
    // Limpia el canvas
    context.clearRect(0, 0, mainCanvas.width, mainCanvas.height);
    var valorPrediccionElement = document.getElementById('valor-prediccion');
    valorPrediccionElement.textContent = ''
  });

  const predictButton = document.getElementById('predict-button');
  const imagenDibujadaInput = document.getElementById('imagen-dibujada');

  predictButton.addEventListener('click', function() {
      // Obtén la imagen en formato Base64
      const imagenBase64 = mainCanvas.toDataURL("image/png");

      // Asigna la imagen Base64 al campo "imagen" del formulario
      imagenDibujadaInput.value = imagenBase64;
  });

});
