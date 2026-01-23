from db.postgres import cursor


def insert_impression(impression):
    cursor.execute("""
        INSERT INTO ad_impressions
        (impression_id, ad_category, device_type, timestamp, clicked)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        str(impression["impression_id"]),   # 🔧 FIX HERE
        impression["ad_category"],
        impression["device_type"],
        impression["timestamp"],
        impression["clicked"]
    ))
