from fastapi import APIRouter
from datetime import datetime
import uuid

from api.schemas import AdRequest, ClickPredictionRequest
from processing.processor import generate_impression
from processing.db_writer import insert_impression
from processing.aggregator import aggregate_metrics
from ml.predict import predict_click
from db.mongo import raw_requests_collection

router = APIRouter()

# -------------------------------------------------
# Ad Ingestion Endpoint
# -------------------------------------------------
@router.post("/ad-request")
def ingest_ad_request(payload: AdRequest):
    """
    Receives a full ad request, stores it, processes impression,
    aggregates metrics, and returns click result.
    """

    # Convert payload to dict
    ad_data = payload.dict()

    # Store raw event in MongoDB
    raw_requests_collection.insert_one(ad_data)

    # Simulate impression + click
    impression = generate_impression(ad_data)

    # Store impression in PostgreSQL
    insert_impression(impression)

    # Aggregate metrics
    aggregate_metrics(impression)

    return {
        "status": "success",
        "clicked": impression["clicked"]
    }


# -------------------------------------------------
# ML Click Prediction Endpoint
# -------------------------------------------------
@router.post("/predict-click")
def predict_click_api(payload: ClickPredictionRequest):
    """
    Predicts click probability using trained ML model.
    """

    features = payload.dict()
    prediction = predict_click(features)

    return prediction
