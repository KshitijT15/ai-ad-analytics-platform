from db.postgres import cursor
from datetime import datetime, timedelta


def aggregate_metrics():
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=1)

    cursor.execute("""
        SELECT ad_category,
               COUNT(*) AS impressions,
               SUM(CASE WHEN clicked THEN 1 ELSE 0 END) AS clicks
        FROM ad_impressions
        WHERE timestamp BETWEEN %s AND %s
        GROUP BY ad_category
    """, (start_time, end_time))

    results = cursor.fetchall()

    for ad_category, impressions, clicks in results:
        ctr = clicks / impressions if impressions else 0

        cursor.execute("""
            INSERT INTO aggregated_metrics
            (time_window, ad_category, impressions, clicks, ctr)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (time_window, ad_category)
            DO UPDATE SET
                impressions = EXCLUDED.impressions,
                clicks = EXCLUDED.clicks,
                ctr = EXCLUDED.ctr
        """, (
            start_time,
            ad_category,
            impressions,
            clicks,
            ctr
        ))
