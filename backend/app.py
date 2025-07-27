from flask import Flask, request, jsonify
from joblib import load
from function import *
import os
import subprocess
import pandas as pd
from flask_cors import CORS
from waitress import serve

app = Flask(__name__)
CORS(app)  

subprocess.run(["python", "download_model.py"])
# model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'password_strength_model_v2.joblib'))

try:
    model = load("models/password_strength_model_v2.joblib")
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)
        if not data or 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        
        password = data['password']
        df = pd.DataFrame({'pw': [password]})
        prediction = model.predict(df)

        return jsonify({
            'strength': prediction[0],
            'message': f"Your password is {prediction[0]}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    print("Server is running on http://localhost:5000")
    serve(app, host='0.0.0.0', port=5000)
