"""
config.py
Week 2 – Customer Experience Analytics

Configuration for scraping Google Play reviews for:
- CBE
- Bank of Abyssinia
- Dashen Bank
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional; if it's not installed, continue without loading a .env file
    def load_dotenv():
        return

# Google Play app IDs (override via .env if needed)
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
    # target scraped per bank (you’ll likely end up with 400+ usable reviews)
    "reviews_per_bank": int(os.getenv("REVIEWS_PER_BANK", 600)),
    "lang": "en",        # you can later add 'am' etc. if you want multi-language
    "country": "et",
    "max_retries": int(os.getenv("MAX_RETRIES", 3)),
}

DATA_PATHS = {
    "raw_dir": "data/raw",
    "raw_reviews": "data/raw/reviews_raw.csv",
    "app_info": "data/raw/app_info.csv",
}
