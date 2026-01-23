import os
import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

# ---------- FIXED BASE DIRECTORY ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "click_prediction_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "encoders.pkl")

# ---------- DATABASE CONNECTION ----------
conn = psycopg2.connect(
    dbname="ad_analytics",
    user="postgres",
    password="newpassword123",
    host="localhost",
    port=5432
)

# ---------- LOAD TRAINING DATA ----------
query = "SELECT * FROM ml_training_data;"
df = pd.read_sql(query, conn)

if df.empty:
    raise ValueError("❌ No training data found in ml_training_data table")

# ---------- ENCODE CATEGORICAL FEATURES ----------
encoders = {}
categorical_cols = ["device_type", "location", "ad_category"]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# ---------- FEATURES & TARGET ----------
X = df.drop("clicked", axis=1)
y = df["clicked"]

# ---------- TRAIN / TEST SPLIT ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------- TRAIN MODEL ----------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# ---------- EVALUATION ----------
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy:.2f}")

# ---------- SAVE MODEL (CORRECT LOCATION) ----------
joblib.dump(model, MODEL_PATH)
joblib.dump(encoders, ENCODER_PATH)

print("✅ ML model trained successfully")
print("📦 Model saved at:", MODEL_PATH)
print("📦 Encoders saved at:", ENCODER_PATH)
