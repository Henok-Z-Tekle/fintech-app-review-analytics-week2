# Task 1 — Data Collection and Preprocessing

This repository contains code to collect and preprocess Google Play Store reviews for several banking apps.

High-level steps:

- Use `scripts/scrape_reviews.py` to collect reviews for app IDs. It saves per-app CSV files into `data/raw/`.
- Use `scripts/preprocess.py` to combine the raw CSVs, remove duplicates and missing data, normalize dates, and write `data/processed/reviews_clean.csv`.

Quick start

1. Create and activate a Python virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Scrape reviews (example for three bank apps — replace with actual package names):

```powershell
python scripts/scrape_reviews.py --apps com.bank.a com.bank.b com.bank.c --count 500 --output data/raw/
```

3. Preprocess and combine the CSVs:

```powershell
python scripts/preprocess.py --raw data/raw/ --out data/processed/reviews_clean.csv
```

Methodology (brief)

- Web scraping: Use `google_play_scraper` to collect reviews, ratings, dates, and user metadata where available. Target at least 400 reviews per bank to meet the assignment KPI.
- Preprocessing: Remove duplicate reviews, drop rows missing review text, coerce/normalize dates to `YYYY-MM-DD`, and save a single clean CSV with columns `review`, `rating`, `date`, `bank`, `source`.
- Version control: Work on the `task-1` branch and commit frequently with meaningful messages.

Next steps

- Add a small driver and scheduling to run scrapes in parallel with rate limiting.
- Add unit tests for preprocessing logic.
