from pydantic import BaseModel
from datetime import datetime
from typing import Literal


# -----------------------------
# Ad Ingestion Schema
# -----------------------------
class AdRequest(BaseModel):
    request_id: str
    user_id: str
    device_type: Literal["mobile", "desktop", "tablet"]
    location: str
    timestamp: datetime
    ad_category: str
    publisher_id: str


# -----------------------------
# ML Prediction Schema
# -----------------------------
class ClickPredictionRequest(BaseModel):
    device_type: Literal["mobile", "desktop", "tablet"]
    location: str
    ad_category: str
    hour: int
    impressions: int
