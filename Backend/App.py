from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image, UnidentifiedImageError

# Inicializa la aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Carga el modelo entrenado
MODEL_PATH = "model/model/climate_classifier.h5"
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo desde {MODEL_PATH}: {e}")

# Clases del modelo
CLASSES = [
    'rain', 'rime', 'dew', 'hail', 'frost', 
    'sandstorm', 'glaze', 'fogsmog', 
    'lightning', 'snow', 'rainbow'
]

# Función de predicción
def predict_image(image):
    try:
        image = image.resize((64, 64))  # Redimensionar la imagen
        image = np.array(image) / 255.0  # Normalizar
        image = np.expand_dims(image, axis=0)  # Expandir dimensiones
        predictions = model.predict(image)
        class_index = np.argmax(predictions)
        confidence = round(np.max(predictions) * 100, 2)
        return CLASSES[class_index], confidence
    except Exception as e:
        raise ValueError(f"Error al procesar la imagen para predicción: {e}")

# Endpoint para clasificar imágenes
@app.route("/api/image-classification", methods=["POST"])
def classify_image():
    if "file" not in request.files:
        return jsonify({"error": "No se subió ninguna imagen"}), 400

    file = request.files["file"]

    try:
        # Cargar y procesar la imagen
        image = Image.open(file.stream).convert("RGB")
        class_name, confidence = predict_image(image)
        return jsonify({"class": class_name, "confidence": confidence}), 200
    except UnidentifiedImageError:
        return jsonify({"error": "El archivo proporcionado no es una imagen válida"}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500

# Ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True, port=5000)
