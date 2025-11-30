"""Scrape Google Play reviews for given app ids and save CSVs.

Usage:
  python scripts/scrape_reviews.py --apps com.bank.example1 com.bank.example2 --count 500 --output data/raw/

This uses the `google_play_scraper` package (already listed in `requirements.txt`).
"""
import argparse
import time
from pathlib import Path

import pandas as pd
from google_play_scraper import Sort, reviews


def scrape_app(app_id: str, count: int = 400, lang: str = "en", country: str = "us") -> pd.DataFrame:
    """Scrape up to `count` reviews for an app and return a DataFrame.
    Columns: review, rating, date, userName, replyDate, replyContent
    """
    result = []
    continuation_token = None
    while len(result) < count:
        to_fetch = min(200, count - len(result))
        r, continuation_token = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=Sort.NEWEST,
            count=to_fetch,
            continuation_token=continuation_token,
        )
        if not r:
            break
        result.extend(r)
        time.sleep(0.5)

    rows = []
    for item in result:
        rows.append({
            "review": item.get("content"),
            "rating": item.get("score"),
            "date": item.get("at"),
            "userName": item.get("userName"),
            "replyDate": item.get("replyAt"),
            "replyContent": item.get("replyContent"),
        })

    df = pd.DataFrame(rows)
    # Ensure date column is datetime
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apps", nargs="+", required=True, help="One or more app IDs to scrape")
    parser.add_argument("--count", type=int, default=400, help="Number of reviews per app")
    parser.add_argument("--output", default="data/raw/", help="Output folder for raw CSVs")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--country", default="us")
    args = parser.parse_args()

    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)

    for app_id in args.apps:
        print(f"Scraping {app_id}... (target {args.count} reviews)")
        df = scrape_app(app_id, count=args.count, lang=args.lang, country=args.country)
        # If date is datetime, convert to ISO date strings
        if not df.empty and pd.api.types.is_datetime64_any_dtype(df["date"]):
            df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        filename = outdir / f"{app_id.replace('.', '_')}.csv"
        df.to_csv(filename, index=False)
        print(f"Saved {len(df)} reviews to {filename}")


if __name__ == "__main__":
    main()
