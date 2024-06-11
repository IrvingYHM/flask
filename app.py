from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Cargar el modelo entrenado
try:
    modelo = joblib.load("modelo_apple_quality.pkl")
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
        data = request.get_json()
        # Crear el DataFrame con los datos recibidos
        X_test = pd.DataFrame(data)
        
        # Realizar la predicción
        prediction = modelo.predict(X_test)
        
        # Mapeo de la predicción a etiquetas de calidad
        quality_mapping = {0: 'mala', 1: 'buena'}
        prediction_label = [quality_mapping[pred] for pred in prediction]
        
        # Construir el mensaje de respuesta
        prediction_message = f"La manzana es de {prediction_label[0]} calidad"
        
        return jsonify({'message': prediction_message})
    except Exception as e:
        print(f"Error en la predicción: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
