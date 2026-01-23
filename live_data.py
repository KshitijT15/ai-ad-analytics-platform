import time
import psycopg2
import random
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    database="ad_analytics",
    user="postgres",
    password="newpassword123"
)
cur = conn.cursor()

while True:
    impressions = random.randint(80, 150)
    clicks = random.randint(0, impressions // 2)
    predicted_ctr = (clicks / impressions) * 0.9

    # insert actual data
    cur.execute("""
        INSERT INTO aggregated_metrics (time_window, ad_category, impressions, clicks)
        VALUES (%s, %s, %s, %s)
    """, (datetime.now(), 'tech', impressions, clicks))

    # insert prediction
    cur.execute("""
        INSERT INTO ml_ctr_predictions (time_window, ad_category, predicted_ctr)
        VALUES (%s, %s, %s)
    """, (datetime.now(), 'tech', predicted_ctr))

    conn.commit()
    print("Inserted live data")

    time.sleep(60)   # every 1 minute
