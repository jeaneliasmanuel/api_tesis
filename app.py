from flask import Flask, request, jsonify
from flask_cors import CORS  # Necesitas instalar flask-cors
import tensorflow as tf
import numpy as np
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas por defecto

# Cargar el modelo TensorFlow
modelo = tf.keras.models.load_model('az_detectitonv2.h5')

def preparar_imagen(base64_img):
    # Convertir base64 a bytes
    img_bytes = base64.b64decode(base64_img)
    # Abrir la imagen como un objeto PIL
    img = Image.open(BytesIO(img_bytes))

    # Redimensionar la imagen de acuerdo a la escala de su tamaño original
    img = img.resize((176//2, 208//2))

    # Convertir la imagen a un arreglo de NumPy
    img = np.array(img)

    # Normalizar la imagen
    img = img / 255.0

    return img

@app.route('/', methods=['POST'])
def predecir():
    try:
        # Intenta obtener los datos JSON de la solicitud
        datos = request.get_json()
        if not datos or 'imagen' not in datos:
            return jsonify({'error': 'No se proporcionó la clave imagen en el JSON'}), 400

        imagen64 = datos['imagen']
        imgagen64_list = imagen64.split(",")

        img_base64 = imgagen64_list[-1]

        # Preparar la imagen
        imagen = preparar_imagen(img_base64)

        # Realizar la predicción
        prediccion = modelo.predict(np.array([imagen]))
        valores_prediccion = [float(valor) for valor in prediccion[0]]
    
    except Exception as e:
        # Maneja cualquier otro error (por ejemplo, JSON mal formado)
        return jsonify({'error': str(e)}), 400

    return jsonify({'resultado': valores_prediccion})

@app.route('/', methods=['GET'])
def hello_world():
    return "Hello World"

@app.route('/<name>', methods=['GET'])
def hello_name(name):
    if not name:
        name = "?"
    return "Hello "+ name


if __name__ == '__main__':
    app.run(debug=True)
