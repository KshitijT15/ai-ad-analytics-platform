import os
import joblib
import pandas as pd

# ---------- PATH SETUP ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "click_prediction_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "encoders.pkl")

# ---------- LOAD MODEL & ENCODERS ----------
model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)

FEATURE_ORDER = ["device_type", "location", "ad_category", "hour", "impressions"]

# ---------- PREDICTION FUNCTION ----------
def predict_click(payload: dict):
    data = payload.copy()

    # Encode categorical features
    for col in ["device_type", "location", "ad_category"]:
        if col in encoders:
            data[col] = encoders[col].transform([data[col]])[0]

    df = pd.DataFrame([data], columns=FEATURE_ORDER)

    prob = model.predict_proba(df)[0][1]
    prediction = bool(prob >= 0.5)

    return {
        "click_probability": round(float(prob), 3),
        "predicted_click": prediction
    }
