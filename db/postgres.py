import psycopg2

conn = psycopg2.connect(
    dbname="ad_analytics",
    user="postgres",
    password="newpassword123",
    host="localhost",
    port="5432"
)

conn.autocommit = True
cursor = conn.cursor()
