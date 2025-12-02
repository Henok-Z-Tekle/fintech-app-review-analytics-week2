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
import os

# Import config for canonical data paths and bank mappings. Support running as script or package.
try:
    from config import APP_IDS, BANK_NAMES, DATA_PATHS
except Exception:
    from ..src.config import APP_IDS, BANK_NAMES, DATA_PATHS


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
        bank_code = f.stem
        # Try to map filename/app id to known bank code (APP_IDS values may be app ids)
        # If filename contains an app id, try to invert APP_IDS
        inv = {v: k for k, v in APP_IDS.items()}
        if bank_code in inv:
            bank_code = inv[bank_code]

        df["bank_code"] = bank_code
        df["bank_name"] = BANK_NAMES.get(bank_code, bank_code)
        df["source"] = "google_play"

        # Keep and standardize relevant columns
        # Map common names to canonical names
        col_map2 = {}
        if "review" in df.columns and "review_text" not in df.columns:
            col_map2["review"] = "review_text"
        if "date" in df.columns and "review_date" not in df.columns:
            col_map2["date"] = "review_date"
        if "rating" in df.columns and "rating" not in df.columns:
            col_map2["rating"] = "rating"
        df = df.rename(columns=col_map2)

        keep = [c for c in ["review_text", "rating", "review_date", "bank_code", "bank_name", "source"] if c in df.columns]
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

    # Ensure dates normalized in final file
    if "review_date" in combined.columns:
        combined["review_date"] = pd.to_datetime(combined["review_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # Write to configured processed path if available
    processed_path = out_file
    if isinstance(DATA_PATHS, dict) and DATA_PATHS.get("processed_reviews"):
        processed_path = Path(DATA_PATHS["processed_reviews"])

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(processed_path, index=False)
    print(f"Saved cleaned data ({len(combined)} rows) to {processed_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default="data/raw/", help="Folder with raw CSVs")
    parser.add_argument("--out", default="data/processed/reviews_clean.csv", help="Output cleaned CSV")
    args = parser.parse_args()

    preprocess(Path(args.raw), Path(args.out))


if __name__ == "__main__":
    main()
