from db.postgres import cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS ad_impressions (
    impression_id UUID PRIMARY KEY,
    ad_category VARCHAR(50),
    device_type VARCHAR(20),
    timestamp TIMESTAMP,
    clicked BOOLEAN
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS aggregated_metrics (
    time_window TIMESTAMP,
    ad_category VARCHAR(50),
    impressions INT,
    clicks INT,
    ctr FLOAT,
    PRIMARY KEY (time_window, ad_category)
);
""")

print("Database tables initialized")
