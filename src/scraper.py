"""
scraper.py
Task 1 – Google Play review scraping for:
CBE, BOA, Dashen Bank

Usage:
    python src/scraper.py
"""

import os
import sys
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from tqdm import tqdm
from google_play_scraper import app, reviews, Sort

from config import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS


class ReviewScraper:
    def __init__(self) -> None:
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES

        # ✅ pulled from config (already set to 400 / en / et)
        self.reviews_per_bank = SCRAPING_CONFIG["reviews_per_bank"]
        self.lang = SCRAPING_CONFIG["lang"]
        self.country = SCRAPING_CONFIG["country"]
        self.max_retries = SCRAPING_CONFIG["max_retries"]

    def _ensure_dirs(self) -> None:
        os.makedirs(DATA_PATHS["raw_dir"], exist_ok=True)

    # ---------- app info ----------

    def get_app_info(self, app_id: str, bank_code: str) -> Optional[Dict[str, Any]]:
        try:
            info = app(app_id, lang=self.lang, country=self.country)
        except Exception as e:
            print(f"[ERROR] Failed to get app info for {bank_code}: {e}")
            return None

        return {
            "bank_code": bank_code,
            "bank_name": self.bank_names[bank_code],
            "app_id": app_id,
            "title": info.get("title", ""),
            "score": info.get("score", None),
            "ratings": info.get("ratings", None),
            "reviews": info.get("reviews", None),
            "installs": info.get("installs", ""),
            "scraped_at": datetime.utcnow().isoformat(),
        }

    # ---------- review scraping ----------

    def scrape_reviews_for_app(self, app_id: str, bank_code: str) -> List[Dict[str, Any]]:
        print(f"\n[INFO] Scraping {self.bank_names[bank_code]} ({app_id})...")
        attempt = 0
        while attempt < self.max_retries:
            try:
                raw_reviews, _ = reviews(
                    app_id,
                    lang=self.lang,       # ✅ en
                    country=self.country,  # ✅ et
                    sort=Sort.NEWEST,
                    count=self.reviews_per_bank,  # ✅ 400
                    filter_score_with=None,
                )
                break
            except Exception as e:
                attempt += 1
                print(f"[WARN] Attempt {attempt}/{self.max_retries} failed: {e}")
                if attempt == self.max_retries:
                    print(f"[ERROR] Giving up on {bank_code}")
                    return []
                time.sleep(5)

        processed: List[Dict[str, Any]] = []
        for r in raw_reviews:
            processed.append(
                {
                    "review_id": r.get("reviewId", ""),
                    "review_text": r.get("content", ""),
                    "rating": r.get("score", None),
                    "review_date": r.get("at").isoformat() if r.get("at") else None,
                    "user_name": r.get("userName", "Anonymous"),
                    "thumbs_up": r.get("thumbsUpCount", 0),
                    "reply_content": r.get("replyContent", None),
                    "bank_code": bank_code,
                    "bank_name": self.bank_names[bank_code],
                    "app_version": r.get("reviewCreatedVersion", ""),
                    "source": "Google Play",
                }
            )
        return processed

    # ---------- main run ----------

    def run(self) -> pd.DataFrame:
        self._ensure_dirs()

        all_app_info: List[Dict[str, Any]] = []
        all_reviews: List[Dict[str, Any]] = []

        print("=" * 70)
        print("Week 2 – Google Play Review Scraper")
        print("=" * 70)

        # 1) App metadata
        print("\n[STEP 1/2] Fetching app metadata...")
        for code, app_id in self.app_ids.items():
            info = self.get_app_info(app_id, code)
            if info:
                all_app_info.append(info)
                print(
                    f"  {code}: {info['title']} | "
                    f"⭐ {info['score']} ({info['ratings']} ratings, {info['reviews']} reviews)"
                )

        if all_app_info:
            app_info_df = pd.DataFrame(all_app_info)
            app_info_df.to_csv(DATA_PATHS["app_info"], index=False)
            print(f"[INFO] Saved app info → {DATA_PATHS['app_info']}")

        # 2) Reviews
        print("\n[STEP 2/2] Scraping reviews...")
        for code, app_id in tqdm(self.app_ids.items(), desc="Banks"):
            bank_reviews = self.scrape_reviews_for_app(app_id, code)
            all_reviews.extend(bank_reviews)
            time.sleep(2)

        if not all_reviews:
            print("\n[FATAL] No reviews scraped.")
            return pd.DataFrame()

        df = pd.DataFrame(all_reviews)
        df["scraped_at"] = datetime.utcnow().isoformat()

        df.to_csv(DATA_PATHS["raw_reviews"], index=False)
        print(f"\n[INFO] Saved raw reviews → {DATA_PATHS['raw_reviews']}")

        print("\nReview counts per bank:")
        print(df["bank_name"].value_counts())

        return df


def main() -> None:
    scraper = ReviewScraper()
    df = scraper.run()
    if df.empty:
        print("\n✗ Scraping failed.")
    else:
        print("\n✓ Scraping completed successfully.")


if __name__ == "__main__":
    main()
