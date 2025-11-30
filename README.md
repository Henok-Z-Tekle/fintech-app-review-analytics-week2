# Fintech App Review Analytics — Task 1

This repository implements Task 1: collecting and preprocessing Google Play Store reviews for Ethiopian banking apps, preparing a clean dataset ready for NLP and analysis.

Key goals

- Collect at least 400+ reviews per target bank (3 banks → 1,200+ reviews total).
- Produce a cleaned CSV with columns: `review_text`, `rating`, `review_date`, `bank_code`, `bank_name`, `source`.
- Keep the workflow reproducible and version controlled on the `task-1` branch.

Repository layout

- `scripts/` — CLI scripts to scrape (`scrape_reviews.py`) and preprocess (`preprocess.py`).
- `src/` — library modules and notebooks (`scraper.py`, `preprocessing.py`, `preprocessing_EDA.ipynb`).
- `data/raw/` — raw per-app CSVs created by the scraper.
- `data/processed/` — cleaned and combined CSVs for analysis.
- `requirements.txt` — Python dependencies.

Quick start (local)

1. Create and activate a Python virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Scrape reviews for apps (example):

```powershell
python scripts/scrape_reviews.py --apps com.combanketh.mobilebanking com.boa.boaMobileBanking com.dashen.dashensuperapp --count 500 --output data/raw/
```

3. Preprocess the raw CSV files to create a clean dataset:

```powershell
python scripts/preprocess.py --raw data/raw/ --out data/processed/reviews_clean.csv
```

4. Run exploratory analysis notebook:

```powershell
# Open `src/preprocessing_EDA.ipynb` in Jupyter or VS Code and run cells.
```

Database (optional)

- If you prefer storing data in PostgreSQL, set environment variables and use `src/db_connection.py` and `src/scraper.py` to write to the DB. Example environment variables:

```powershell
setx DB_HOST localhost
setx DB_PORT 5432
setx DB_NAME bank_reviews
setx DB_USER postgres
setx DB_PASSWORD 'your_password'
```

Insights & methodology

- Scraping: We use `google_play_scraper` to fetch review text, rating, timestamps, and metadata. Scraping parameters (language, country, reviews per bank) are configured in `src/config.py`.
- Preprocessing: Scripts remove duplicates, drop reviews missing critical fields, normalize dates to `YYYY-MM-DD`, compute text-length features, and produce a clean CSV suitable for NLP pipelines.
- KPIs: Aim for >=400 reviews per bank and <5% missing critical fields after preprocessing.

Troubleshooting

- If imports fail for optional packages like `google_play_scraper` or `python-dotenv`, install them via `pip install google-play-scraper python-dotenv`.
- If the scraper returns fewer reviews than expected, try increasing `reviews_per_bank` in `src/config.py` or inspect app availability on Google Play.

Next steps

- Add sentiment analysis and topic modeling notebooks.
- Add unit tests for preprocessing and a CI workflow to run import/syntax checks on push.

If you'd like, I can open a PR from `task-1` into `main` after pushing these updates.
