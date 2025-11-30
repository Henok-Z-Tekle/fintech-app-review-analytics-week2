"""
config.py
Week 2 – Customer Experience Analytics
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ---------- Google Play scraping ----------

APP_IDS = {
    "CBE": os.getenv("CBE_APP_ID", "com.combanketh.mobilebanking"),
    "BOA": os.getenv("BOA_APP_ID", "com.boa.boaMobileBanking"),
    "Dashen": os.getenv("DASHEN_APP_ID", "com.dashen.dashensuperapp"),
}

BANK_NAMES = {
    "CBE": "Commercial Bank of Ethiopia",
    "BOA": "Bank of Abyssinia",
    "Dashen": "Dashen Bank",
}

SCRAPING_CONFIG = {
    # ✅ as you requested
    "reviews_per_bank": 400,
    "lang": "en",
    "country": "et",
    "max_retries": int(os.getenv("MAX_RETRIES", 3)),
}

DATA_PATHS = {
    "raw_dir": "data/raw",
    "raw_reviews": "data/raw/reviews_raw.csv",
    "app_info": "data/raw/app_info.csv",
    "processed_dir": "data/processed",
    "processed_reviews": "data/processed/reviews_processed.csv",
    "sentiment_reviews": "data/processed/reviews_with_sentiment.csv",
}

# ---------- PostgreSQL DB config ----------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),      # ✅ 5432
    "dbname": os.getenv("DB_NAME", "bank_reviews"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "Henzi19$"),  # ✅ default as requested
}
