# AquaSafe 🌊
**Cloud-Based Water Quality Monitoring & Contamination Prediction**

## 📌 Project Objective
AquaSafe is a full-stack AI application that predicts whether a water sample is **Safe** or **Contaminated**.  
It uses a **Random Forest Classifier** trained on real water quality data and serves predictions via a **Flask API** and a **Web Interface**.

---

## 🚀 Quick Start Guide

### 1. Prerequisite: Install Dependencies
Open a terminal in the `AquaSafe/` folder and run:
```bash
pip install -r requirements.txt
```

### 2. Step 1: Train the Model
You must run the training script once to generate the AI model:
```bash
python model/train_model.py
```
*Wait for the message: "Done. Model saved to model/trained_model.pkl"*

### 3. Step 2: Start the Backend Server
Run the Flask API:
```bash
python backend/app.py
```
✅ The server will start at `http://127.0.0.1:5000`

### 4. Step 3: Launch the Frontend
You have two options:

**Option A: Using Live Server (Recommended)**
1. Open the **root folder** (`Water_Contamination_ML-master`) in VS Code.
2. Click **"Go Live"** (Live Server).
3. The app will automatically open at `http://127.0.0.1:5500/AquaSafe/frontend/index.html` thanks to the redirect.

**Option B: Manual Open**
1. Navigate to `AquaSafe/frontend/`
2. Double-click `index.html` to open it in your browser.

---

## 📂 Project Structure
```
AquaSafe/
├── data/
│   └── Water_contamination.csv  # Dataset
├── model/
│   ├── train_model.py           # Training logic
│   └── trained_model.pkl        # The AI Model
├── backend/
│   └── app.py                   # Flask API (Port 5000)
├── frontend/
│   ├── index.html               # UI Entry Point
│   ├── style.css                # Styling
│   └── script.js                # Frontend Logic
└── requirements.txt             # Dependencies
```

## 🛠 Troubleshooting
- **"Failed to connect to server"**: Ensure the backend terminal is running `backend/app.py`.
- **Directory listing instead of App**: Open the root folder in VS Code and use Live Server. The `index.html` in the root will redirect you correctly.
