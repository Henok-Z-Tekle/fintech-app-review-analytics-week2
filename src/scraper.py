"""
Google Play Store Review Scraper
Task 1: Data Collection

This script scrapes user reviews from Google Play Store for three Ethiopian banks.
Target: 400+ reviews per bank (minimum).

Usage:
    python -m src.scraper
or:
    python src/scraper.py
"""

import sys
import os
from typing import Any, Dict, List, Optional

# Allow importing config when running as a script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google_play_scraper import app, Sort, reviews
import pandas as pd
from datetime import datetime
import time
try:
    from tqdm import tqdm
except Exception:
    # Provide a lightweight fallback if tqdm is not available in the environment
    def tqdm(iterable, **kwargs):
        return iterable
from config import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS


class PlayStoreScraper:
    """Scraper class for Google Play Store reviews."""

    def __init__(self) -> None:
        # Load configuration variables from config
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES
        # Use .get to provide defaults in case keys are missing
        self.reviews_per_bank = SCRAPING_CONFIG.get("reviews_per_bank", 400)
        self.lang = SCRAPING_CONFIG.get("lang", "en")
        self.country = SCRAPING_CONFIG.get("country", "et")
        self.max_retries = SCRAPING_CONFIG.get("max_retries", 3)
        # Data paths (ensure backward compatibility with older key names)
        self.raw_dir = DATA_PATHS.get("raw_dir", DATA_PATHS.get("raw", "data/raw"))
        self.raw_reviews_path = DATA_PATHS.get("raw_reviews", os.path.join(self.raw_dir, "reviews_raw.csv"))
        self.app_info_path = DATA_PATHS.get("app_info", os.path.join(self.raw_dir, "app_info.csv"))

    def get_app_info(self, app_id: str) -> Optional[Dict[str, Any]]:
        """Get basic information about the app (rating, total reviews, etc.)."""
        try:
            result = app(app_id, lang=self.lang, country=self.country)
            return {
                "app_id": app_id,
                "title": result.get("title", "N/A"),
                "score": result.get("score", 0),
                "ratings": result.get("ratings", 0),
                "reviews": result.get("reviews", 0),
                "installs": result.get("installs", "N/A"),
            }
        except Exception as e:
            print(f"[ERROR] Getting app info for {app_id}: {e}")
            return None

    def scrape_reviews(self, app_id: str, count: int) -> List[Dict[str, Any]]:
        """
        Scrape reviews for a specific app.

        Attempts to fetch `count` number of reviews, sorted by newest first.
        Includes a retry mechanism for stability.
        """
        print(f"\n[INFO] Scraping reviews for app_id={app_id} ...")

        for attempt in range(self.max_retries):
            try:
                result, _ = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=count,
                    filter_score_with=None,  # all ratings (1–5)
                )
                print(f"[INFO] Successfully scraped {len(result)} reviews")
                return result
            except Exception as e:
                print(f"[WARN] Attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    print("[INFO] Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print("[ERROR] Failed to scrape reviews after max retries")

        return []

    def process_reviews(self, reviews_data: List[Dict[str, Any]], bank_code: str) -> List[Dict[str, Any]]:
        """
        Process raw review data into a clean dictionary format.

        Extracts only relevant fields needed for analysis.
        """
        processed: List[Dict[str, Any]] = []

        for review in reviews_data:
            processed.append(
                {
                    "review_id": review.get("reviewId", ""),
                    "review_text": review.get("content", ""),
                    "rating": review.get("score", 0),
                    "review_date": review.get("at", datetime.now()),
                    "user_name": review.get("userName", "Anonymous"),
                    "thumbs_up": review.get("thumbsUpCount", 0),
                    "reply_content": review.get("replyContent", None),
                    "bank_code": bank_code,
                    "bank_name": self.bank_names[bank_code],
                    # reviewCreatedVersion is actually the app version, not the app ID
                    "app_version": review.get("reviewCreatedVersion", "N/A"),
                    "source": "Google Play",
                }
            )

        return processed

    def scrape_all_banks(self) -> pd.DataFrame:
        """
        Orchestrates scraping:
        1. Fetch app metadata for each bank
        2. Scrape reviews for each app
        3. Save raw CSV(s)
        """
        all_reviews: List[Dict[str, Any]] = []
        app_info_list: List[Dict[str, Any]] = []

        print("=" * 60)
        print("Starting Google Play Store Review Scraper")
        print("=" * 60)

        # Phase 1: fetch app info
        print("\n[1/2] Fetching app information...")
        for bank_code, app_id in self.app_ids.items():
            print(f"\n{bank_code}: {self.bank_names[bank_code]}")
            print(f"App ID: {app_id}")

            info = self.get_app_info(app_id)
            if info:
                info["bank_code"] = bank_code
                info["bank_name"] = self.bank_names[bank_code]
                app_info_list.append(info)
                print(f"Current Rating: {info['score']}")
                print(f"Total Ratings: {info['ratings']}")
                print(f"Total Reviews: {info['reviews']}")

        # Save app info
        if app_info_list:
            app_info_df = pd.DataFrame(app_info_list)
            os.makedirs(self.raw_dir, exist_ok=True)
            app_info_df.to_csv(self.app_info_path, index=False)
            print(f"\n[INFO] App information saved to {self.app_info_path}")

        # Phase 2: scrape reviews
        print("\n[2/2] Scraping reviews for each bank...")
        for bank_code, app_id in tqdm(self.app_ids.items(), desc="Banks"):
            reviews_data = self.scrape_reviews(app_id, self.reviews_per_bank)

            if reviews_data:
                processed = self.process_reviews(reviews_data, bank_code)
                all_reviews.extend(processed)
                print(f"[INFO] Collected {len(processed)} reviews for {self.bank_names[bank_code]}")
            else:
                print(f"[WARN] No reviews collected for {self.bank_names[bank_code]}")

            time.sleep(2)  # polite delay

        # Phase 3: save raw reviews
        if all_reviews:
            df = pd.DataFrame(all_reviews)
            os.makedirs(self.raw_dir, exist_ok=True)
            df.to_csv(self.raw_reviews_path, index=False)

            print("\n" + "=" * 60)
            print("Scraping Complete!")
            print("=" * 60)
            print(f"\n[INFO] Total reviews collected: {len(df)}")

            print("\nReviews per bank:")
            for bank_code in self.bank_names.keys():
                count = len(df[df["bank_code"] == bank_code])
                print(f"  {self.bank_names[bank_code]}: {count}")

            print(f"\n[INFO] Data saved to: {self.raw_reviews_path}")
            return df

        print("\n[ERROR] No reviews were collected!")
        return pd.DataFrame()

    def display_sample_reviews(self, df: pd.DataFrame, n: int = 3) -> None:
        """Display sample reviews from each bank to visually inspect data quality."""
        print("\n" + "=" * 60)
        print("Sample Reviews")
        print("=" * 60)

        for bank_code in self.bank_names.keys():
            bank_df = df[df["bank_code"] == bank_code]
            if not bank_df.empty:
                print(f"\n{self.bank_names[bank_code]}:")
                print("-" * 60)
                samples = bank_df.head(n)
                for _, row in samples.iterrows():
                    stars = "⭐" * int(row["rating"])
                    print(f"\nRating: {stars}")
                    print(f"Review: {row['review_text'][:200]}...")
                    print(f"Date: {row['review_date']}")


def main() -> pd.DataFrame:
    """Main execution function for Task 1 scraping."""
    scraper = PlayStoreScraper()
    df = scraper.scrape_all_banks()

    if not df.empty:
        scraper.display_sample_reviews(df)

    return df


if __name__ == "__main__":
    _ = main()
