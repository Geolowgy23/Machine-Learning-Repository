from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Hello, world!"

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from the POST request
    cgpa = request.form.get('cgpa')
    iq = request.form.get('iq')
    profile_score = request.form.get('profile_score')

    # Convert input data to a numpy array for prediction
    try:
        input_query = np.array([[cgpa, iq, profile_score]],dtype=float)
    except ValueError:
        return jsonify({'error': 'Invalid input values. Please enter numeric values for CGPA, IQ, and profile score.'}), 400

    # Predict the result using the loaded model
    result = model.predict(input_query)[0]

    # Return the result in JSON format
    return jsonify({'placement': str(result)})

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000,debug=True)  # Use debug=True during development for easier debugging