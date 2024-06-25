from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Cargar el modelo entrenado
model_path = os.path.join(os.path.dirname(__file__), "Mobile_Phone_prices.pkl")
try:
    modelo = joblib.load(model_path)
except Exception as e:
    modelo = None
    print(f"Error al cargar el modelo: {e}")

@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/predict', methods=['POST'])
def predict():
    if modelo is None:
        return jsonify({'error': 'El modelo no está disponible.'}), 500

    try:
        # Obtener los datos del formulario en formato JSON
        input_data = request.get_json()
        if input_data is None:
            raise ValueError("No se recibieron datos en formato JSON")

        # Convertir los datos del formulario
        title = float(input_data['title'])
        rating = float(input_data['rating'])
        brand = float(input_data['brand'])
        cable = float(input_data['cable'])
        height = float(input_data['height'])
        storage = float(input_data['storage'])
        
        # Crear el DataFrame con los datos recibidos
        data = {
            'title': [title],
            'rating': [rating],
            'brand': [brand],
            'cable': [cable],
            'height': [height],
            'storage': [storage]
        }
        X_test = pd.DataFrame(data)
        
        # Realizar la predicción
        prediction = modelo.predict(X_test)
        
        # Asegurarnos de que prediction sea un numpy array
        prediction = prediction.flatten()  # Aplanamos el array si es necesario
        
        # Construir el mensaje de respuesta
        prediction_message = f"El precio estimado del teléfono móvil es: {prediction[0]:.2f}"
        
        return jsonify({'message': prediction_message})
    except Exception as e:
        print(f"Error en la predicción: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
