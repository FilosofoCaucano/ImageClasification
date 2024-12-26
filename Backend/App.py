from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)
CORS(app)

MODEL_PATH = r"C:\Users\Willi\Downloads\ProyectoClasificadorImagenes\NuevoClasificadorImagenesClima\Backend\model\model\model\climate_classifier_v3.h5"
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo desde {MODEL_PATH}: {e}")

# Asegúrate de que esta lista esté en el orden correcto como se definió durante el entrenamiento
CLASSES = [
    'dew', 'fogsmog', 'frost', 'glaze', 'hail', 
    'lightning', 'rain', 'rainbow', 'rime', 'sandstorm', 'snow'
]

def predict_image(image):
    image = image.resize((128, 128))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    predictions = model.predict(image)
    class_index = np.argmax(predictions)
    confidence = round(np.max(predictions) * 100, 2)
    return CLASSES[class_index], confidence

@app.route("/api/image-classification", methods=["POST"])
def classify_image():
    if "file" not in request.files:
        return jsonify({"error": "No se subió ninguna imagen"}), 400
    file = request.files["file"]
    try:
        image = Image.open(file.stream).convert("RGB")
        class_name, confidence = predict_image(image)
        return jsonify({"class": class_name, "confidence": confidence}), 200
    except UnidentifiedImageError:
        return jsonify({"error": "El archivo proporcionado no es una imagen válida"}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
