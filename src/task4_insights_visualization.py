"""
Task 4 – Insights and Recommendations (Code Side)
-------------------------------------------------

This script:
- Loads enriched review data from Task 2 (reviews_with_sentiment.csv)
  and keyword data (keywords_per_bank.csv).
- Computes:
    * Rating distributions per bank
    * Sentiment distributions per bank
    * Theme frequencies per bank
    * Top keywords per bank (from TF-IDF)
- Generates 3–5 Matplotlib plots and saves them under `figures/`.

Usage (from project root):
    python src/task4_insights_visualization.py
"""

import os
from typing import Tuple

import pandas as pd
import matplotlib.pyplot as plt

from config import DATA_PATHS


FIG_DIR = "figures"


# --------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------

def ensure_fig_dir(path: str = FIG_DIR) -> None:
    """Create figures directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def load_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load reviews_with_sentiment.csv and keywords_per_bank.csv.

    Returns:
        reviews_df, keywords_df
    """
    sentiment_path = DATA_PATHS.get("sentiment_reviews")
    processed_dir = DATA_PATHS["processed_dir"]
    keywords_path = os.path.join(processed_dir, "keywords_per_bank.csv")

    if not sentiment_path or not os.path.exists(sentiment_path):
        raise FileNotFoundError(
            f"Sentiment dataset not found at {sentiment_path}. "
            f"Run Task 2 to generate reviews_with_sentiment.csv."
        )

    if not os.path.exists(keywords_path):
        raise FileNotFoundError(
            f"Keywords dataset not found at {keywords_path}. "
            f"Run Task 2 to generate keywords_per_bank.csv."
        )

    reviews_df = pd.read_csv(sentiment_path)
    keywords_df = pd.read_csv(keywords_path)

    required_cols = {"review_id", "bank_code", "bank_name", "rating",
                     "sentiment_label", "sentiment_score"}
    missing = required_cols - set(reviews_df.columns)
    if missing:
        raise ValueError(f"reviews_with_sentiment.csv missing columns: {missing}")

    if "themes" not in reviews_df.columns:
        print("[WARN] 'themes' column not found. Theme plots will be limited.")

    return reviews_df, keywords_df


# --------------------------------------------------------------------
# Plot functions
# --------------------------------------------------------------------

def plot_rating_distribution(df: pd.DataFrame) -> None:
    """Plot rating distribution per bank."""
    ensure_fig_dir()

    pivot = (
        df.groupby(["bank_name", "rating"])["review_id"]
        .count()
        .reset_index(name="count")
    )

    banks = pivot["bank_name"].unique()
    ratings = sorted(df["rating"].dropna().unique())

    # create one subplot per bank
    n_banks = len(banks)
    fig, axes = plt.subplots(1, n_banks, figsize=(5 * n_banks, 4), sharey=True)

    if n_banks == 1:
        axes = [axes]  # make iterable

    for ax, bank in zip(axes, banks):
        sub = pivot[pivot["bank_name"] == bank]
        counts = [sub[sub["rating"] == r]["count"].sum() for r in ratings]

        ax.bar(ratings, counts)
        ax.set_title(bank)
        ax.set_xlabel("Rating (1–5)")
        ax.set_ylabel("Number of Reviews")
        ax.set_xticks(ratings)

    fig.suptitle("Rating Distribution per Bank")
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "rating_distribution_per_bank.png")
    plt.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[INFO] Saved: {out_path}")


def plot_sentiment_distribution(df: pd.DataFrame) -> None:
    """Plot sentiment (POSITIVE/NEGATIVE) distribution per bank."""
    ensure_fig_dir()

    # Normalize label casing
    df["sentiment_label"] = df["sentiment_label"].str.upper()

    pivot = (
        df.groupby(["bank_name", "sentiment_label"])["review_id"]
        .count()
        .reset_index(name="count")
    )

    banks = pivot["bank_name"].unique()
    labels = ["NEGATIVE", "POSITIVE"]  # enforce order

    n_banks = len(banks)
    fig, axes = plt.subplots(1, n_banks, figsize=(5 * n_banks, 4), sharey=True)

    if n_banks == 1:
        axes = [axes]

    for ax, bank in zip(axes, banks):
        sub = pivot[pivot["bank_name"] == bank]
        counts = [sub[sub["sentiment_label"] == lab]["count"].sum() for lab in labels]

        ax.bar(labels, counts)
        ax.set_title(bank)
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Number of Reviews")

    fig.suptitle("Sentiment Distribution per Bank")
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "sentiment_distribution_per_bank.png")
    plt.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[INFO] Saved: {out_path}")


def plot_themes_per_bank(df: pd.DataFrame) -> None:
    """
    Plot top themes per bank (bar chart).

    Expects a 'themes' column with comma-separated theme names.
    """
    if "themes" not in df.columns:
        print("[WARN] 'themes' column not found. Skipping theme plot.")
        return

    ensure_fig_dir()

    # explode themes into rows
    tmp = df[["bank_name", "themes"]].dropna().copy()
    tmp["themes"] = tmp["themes"].astype(str)
    tmp["theme"] = tmp["themes"].str.split(",")
    tmp = tmp.explode("theme")
    tmp["theme"] = tmp["theme"].str.strip()
    tmp = tmp[tmp["theme"] != ""]

    pivot = (
        tmp.groupby(["bank_name", "theme"])["theme"]
        .count()
        .reset_index(name="count")
    )

    banks = pivot["bank_name"].unique()
    n_banks = len(banks)
    fig, axes = plt.subplots(1, n_banks, figsize=(6 * n_banks, 5), sharey=False)

    if n_banks == 1:
        axes = [axes]

    for ax, bank in zip(axes, banks):
        sub = pivot[pivot["bank_name"] == bank].sort_values("count", ascending=False)
        sub = sub.head(6)  # top 6 themes

        ax.barh(sub["theme"], sub["count"])
        ax.set_title(bank)
        ax.set_xlabel("Count")
        ax.invert_yaxis()  # highest at top

    fig.suptitle("Top Themes per Bank")
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "themes_per_bank.png")
    plt.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[INFO] Saved: {out_path}")


def plot_top_keywords_per_bank(keywords_df: pd.DataFrame, top_n: int = 10) -> None:
    """Plot top TF-IDF keywords per bank (bar chart)."""
    ensure_fig_dir()

    required_cols = {"bank_name", "keyword", "rank"}
    missing = required_cols - set(keywords_df.columns)
    if missing:
        raise ValueError(f"keywords_per_bank.csv missing columns: {missing}")

    banks = keywords_df["bank_name"].unique()
    n_banks = len(banks)
    fig, axes = plt.subplots(1, n_banks, figsize=(6 * n_banks, 5), sharey=False)

    if n_banks == 1:
        axes = [axes]

    for ax, bank in zip(axes, banks):
        sub = keywords_df[keywords_df["bank_name"] == bank]
        sub = sub.sort_values("rank").head(top_n)
        ax.barh(sub["keyword"], top_n - sub["rank"] + 1)  # simple score
        ax.set_title(bank)
        ax.set_xlabel("Keyword Importance (relative)")
        ax.invert_yaxis()

    fig.suptitle(f"Top {top_n} Keywords per Bank")
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "top_keywords_per_bank.png")
    plt.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"[INFO] Saved: {out_path}")


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main() -> None:
    print("=== Task 4 – Insights & Visualizations ===")
    reviews_df, keywords_df = load_datasets()

    print(f"[INFO] Loaded {len(reviews_df)} reviews and {len(keywords_df)} keyword rows.")

    plot_rating_distribution(reviews_df)
    plot_sentiment_distribution(reviews_df)
    plot_themes_per_bank(reviews_df)
    plot_top_keywords_per_bank(keywords_df, top_n=10)

    print("\n[OK] Task 4 plots generated in 'figures/' directory.")
    print("Use these plots in your Week 2 final report for insights & recommendations.")


if __name__ == "__main__":
    main()
