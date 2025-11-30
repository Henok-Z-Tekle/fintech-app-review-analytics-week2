"""
db_connection.py
PostgreSQL connection helper
"""

import psycopg2
from config import DB_CONFIG


def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],         # 5432
            dbname=DB_CONFIG["dbname"],     # bank_reviews
            user=DB_CONFIG["user"],         # postgres
            password=DB_CONFIG["password"]  # Henzi19$
        )
        conn.autocommit = True
        return conn

    except Exception as e:
        print("❌ Failed to connect to PostgreSQL:", e)
        raise
