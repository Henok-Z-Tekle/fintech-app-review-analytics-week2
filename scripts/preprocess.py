"""Preprocess raw review CSVs and create a clean combined CSV.

Actions:
- Read CSVs from `data/raw/`.
- Keep columns: review, rating, date, bank, source.
- Remove duplicates and rows missing review text.
- Normalize dates to YYYY-MM-DD.
- Save to `data/processed/reviews_clean.csv`.
"""
from pathlib import Path
import argparse
import pandas as pd


def preprocess(raw_dir: Path, out_file: Path):
    files = list(raw_dir.glob("*.csv"))
    if not files:
        print(f"No CSV files found in {raw_dir}")
        return

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        # Try to standardize columns
        col_map = {}
        if "content" in df.columns:
            col_map["content"] = "review"
        if "score" in df.columns:
            col_map["score"] = "rating"
        if "at" in df.columns:
            col_map["at"] = "date"
        df = df.rename(columns=col_map)

        # Add bank/source information from filename if possible
        bank = f.stem
        df["bank"] = bank
        df["source"] = "google_play"

        # Keep only relevant columns (if present)
        keep = [c for c in ["review", "rating", "date", "bank", "source"] if c in df.columns]
        df = df[keep]

        dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)

    # Drop rows missing review text
    combined = combined.dropna(subset=["review"])

    # Normalize dates
    if "date" in combined.columns:
        combined["date"] = pd.to_datetime(combined["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # Remove duplicates based on review text + bank
    if "bank" in combined.columns:
        combined = combined.drop_duplicates(subset=["review", "bank"])
    else:
        combined = combined.drop_duplicates(subset=["review"])

    out_file.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(out_file, index=False)
    print(f"Saved cleaned data ({len(combined)} rows) to {out_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default="data/raw/", help="Folder with raw CSVs")
    parser.add_argument("--out", default="data/processed/reviews_clean.csv", help="Output cleaned CSV")
    args = parser.parse_args()

    preprocess(Path(args.raw), Path(args.out))


if __name__ == "__main__":
    main()
