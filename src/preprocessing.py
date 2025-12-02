"""
Task 1 – Preprocessing for Google Play Reviews
Usage:
    python src/preprocessing.py
"""

import os
import pandas as pd
from config import DATA_PATHS


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = " ".join(text.split())
    return text


def main():
    df = pd.read_csv(DATA_PATHS["raw_reviews"])

    # Remove missing critical fields
    df = df.dropna(subset=["review_text", "rating"])

    # Clean text
    df["review_text"] = df["review_text"].apply(clean_text)

    # Date formatting
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    df["review_year"] = df["review_date"].dt.year
    df["review_month"] = df["review_date"].dt.month

    # Text length
    df["text_length"] = df["review_text"].str.len()

    # Remove invalid ratings
    df = df[df["rating"].between(1, 5)]

    os.makedirs(os.path.dirname(DATA_PATHS["raw_reviews"]), exist_ok=True)
    df.to_csv("data/processed/reviews_processed.csv", index=False)

    print("Preprocessing complete. Saved to data/processed/reviews_processed.csv")
    print(df.head())


if __name__ == "__main__":
    main()
