import uuid
import random
from datetime import datetime


def simulate_click(ad_request):
    probability = 0.05

    if ad_request["device_type"] == "mobile":
        probability += 0.05

    if ad_request["ad_category"] == "tech":
        probability += 0.05

    return random.random() < probability


def generate_impression(ad_request):
    return {
        "impression_id": uuid.uuid4(),
        "ad_category": ad_request["ad_category"],
        "device_type": ad_request["device_type"],
        "timestamp": datetime.utcnow(),
        "clicked": simulate_click(ad_request)
    }
