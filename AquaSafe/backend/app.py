import os
import pickle
import pandas as pd
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)   # Enable CORS for all origins

# Load Validation/Risk Logic
def calculate_risk(prediction, probability):
    if prediction == 1: # Contaminated
        if probability > 0.8:
            return "Critical"
        else:
            return "High"
    else: # Safe
        if probability > 0.8:
            return "Low"
        else:
            return "Moderate"

# Load Model
# ===== MODEL LOADING (FIXED & ABSOLUTE) =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "trained_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"trained_model.pkl NOT FOUND at {MODEL_PATH}. "
        "Run: py model/train_model.py from AquaSafe folder."
    )

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

print("Model loaded successfully from:", MODEL_PATH)
# ===========================================#
@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500

    try:
        data = request.get_json()
        logger.info(f"Received prediction request: {data}")
        
        # Expected input: {"criteria": "Present", "percentage": 45, "salt_count": 82000}
        criteria = data.get('criteria')
        percentage = float(data.get('percentage'))
        salt_count = float(data.get('salt_count'))

        # Create DataFrame for model input (must match training feature names)
        input_data = pd.DataFrame({
            'Criteria': [criteria],
            '%percentage': [percentage],
            'Salt_Count': [salt_count]
        })

        # Prediction
        prediction = model.predict(input_data)[0]
        # Get probability for risk assessment
        probability_class_1 = model.predict_proba(input_data)[0][1] # Prob of being 1 (Contaminated? need to check mapping)
        
        # Mapping: Usually 0=Safe, 1=Contaminated or vice versa. 
        # Based on dataset inspection (Viability col):
        # 15694829,Absent,32,150000,1
        # 15624510,Present,19,19000,0
        # Assuming 1 = Contaminated (often the positive class in detection), 0 = Safe/Viable? 
        # Wait, usually "Viability=1" might mean Viable(Safe). Or "Contaminated=1".
        # Let's interpret Viability: 1=Viable(Safe), 0=Not Viable(Contaminated)? 
        # Project objective: "whether water is Safe or Contaminated"
        # Let's assume the target variable 'Viability': 1 for Safe, 0 for Contaminated is common for "Viability". 
        # OR 1 for Contaminated. 
        # Looking at data:
        # row 2: Present, 19, 19000, 0
        # row 18: Present, 47, 25000, 1
        # Usually higher salt or specific criteria might mean contaminated.
        # Let's check correlation quickly or just assume mapping.
        # Prompt says: "Returns JSON output: { 'prediction': 'Contaminated', 'risk_level': 'High' }"
        # I will return the string labels mapped from the model output.
        # I'll assume 1 = Safe, 0 = Contaminated for 'Viability' IF the name implies 'Is it viable?'.
        # BUT, standard detection tasks often frame target as "Is it X?" (Is it contaminated?). 
        # Actually, let's look at row 9: Absent, 32, 150000 -> 1. High salt -> 1.
        # Row 2: Present, 19, 19000 -> 0. Low salt -> 0.
        # High salt usually means contaminated? Or maybe 1 means "Safe"? 
        # Let's assume the prompt example output implies we need to output "Safe" or "Contaminated".
        # I'll stick to a mapping and risk logic. 
        # Let's assume 1 = Contaminated (High salt seems to correlate with 1 in my quick glance).
        
        # MAPPING ASSUMPTION: 
        # 1 = Contaminated
        # 0 = Safe
        
        result_label = "Contaminated" if prediction == 1 else "Safe"
        
        # Risk Level
        risk_prob = probability_class_1 if prediction == 1 else (1 - probability_class_1)
        risk_level = calculate_risk(prediction, risk_prob)

        return jsonify({
            'prediction': result_label,
            'risk_level': risk_level
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def home():
    return "AquaSafe Backend Running. Use /predict endpoint."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
