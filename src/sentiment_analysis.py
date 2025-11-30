"""
Partial Task 2 – Simple Sentiment Labeling
Usage:
    python src/sentiment_analysis.py
"""

import pandas as pd
import os


def rating_to_sentiment(r):
    if r >= 4:
        return "Positive"
    elif r == 3:
        return "Neutral"
    return "Negative"


def main():
    df = pd.read_csv("data/processed/reviews_processed.csv")

    df["sentiment"] = df["rating"].apply(rating_to_sentiment)
    df.to_csv("data/processed/reviews_with_sentiment.csv", index=False)

    print("Saved → data/processed/reviews_with_sentiment.csv")
    print(df["sentiment"].value_counts())


if __name__ == "__main__":
    main()
