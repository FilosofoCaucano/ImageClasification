from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar Flask-CORS
import tensorflow as tf
import numpy as np
from PIL import Image

# Inicializa la aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Carga el modelo entrenado
MODEL_PATH = "model/modelo_clasificacion.h5"  # Ruta al modelo entrenado
model = tf.keras.models.load_model(MODEL_PATH)

# Clases del modelo
CLASSES = ['rain', 'rime', 'dew', 'hail', 'frost', 'sandstorm', 'glaze', 'fogsmog', 'lightning', 'snow', 'rainbow']

# Función de predicción
def predict_image(image):
    image = image.resize((64, 64))  # Redimensionar la imagen
    image = np.array(image) / 255.0  # Normalizar
    image = np.expand_dims(image, axis=0)  # Expandir dimensiones
    predictions = model.predict(image)
    class_index = np.argmax(predictions)
    confidence = round(np.max(predictions) * 100, 2)
    return CLASSES[class_index], confidence

# Endpoint para clasificar imágenes
@app.route("/api/image-classification", methods=["POST"])
def classify_image():
    if "file" not in request.files:
        return jsonify({"error": "No se subió ninguna imagen"}), 400

    file = request.files["file"]
    image = Image.open(file.stream)

    class_name, confidence = predict_image(image)
    return jsonify({"class": class_name, "confidence": confidence})

# Ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True, port=5000)
