# Fintech App Review Analytics — Week 2 (Task 1 & Task 2 roadmap)

This project collects, cleans, and analyzes user reviews from the Google Play Store for Ethiopian banking apps. The primary objective for Week 2 is to deliver a reproducible dataset (400+ usable reviews per bank) and a clean processing pipeline ready for sentiment and thematic analysis.

Quick summary
- Goal: 400+ clean reviews per bank (3 banks → 1,200+). Clean CSV with `review_text`, `rating`, `review_date`, `bank_code`, `bank_name`, `source`.
- Branching: do development on `task-1`, `task-2` branches; merge to `main` with PRs.

Repository structure
- `scripts/`
	- `scrape_reviews.py` — CLI scraper (writes per-app CSVs to `data/raw/`).
	- `preprocess.py` — Combines raw CSVs, removes duplicates/missing fields, normalizes dates, writes `data/processed/reviews_clean.csv`.
- `src/`
	- `scraper.py` — higher-level orchestration module.
	- `preprocessing.py` — `ReviewPreprocessor` class used to clean and validate the dataset.
	- `preprocessing_EDA.ipynb` — exploratory analysis notebook (loads from DB or CSV fallback).
- `data/`
	- `raw/` — raw per-app CSVs
	- `processed/` — cleaned combined CSVs
- `requirements.txt` — pinned project dependencies

Getting started (local, PowerShell)
1. Create and activate a virtual environment and install deps:

```powershell
cd 'C:\Users\heniz\OneDrive\Desktop\KAIM Files\fintech-app-review-analytics-week2'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Scrape reviews (example using configured app IDs in `src/config.py`):

```powershell
# Scrape 400 reviews per app (adjust --count as needed)
python scripts/scrape_reviews.py --apps com.combanketh.mobilebanking com.boa.boaMobileBanking com.dashen.dashensuperapp --count 400 --output data/raw/
```

3. Preprocess to create a clean dataset:

```powershell
python scripts/preprocess.py --raw data/raw/ --out data/processed/reviews_clean.csv
```

4. Run the exploratory notebook for EDA:

```powershell
code src/preprocessing_EDA.ipynb
```

Design & engineering notes
- Config-driven: `src/config.py` centralizes app ids, scraping params, and path config.
- Optional dependencies: the codebase guards optional packages (e.g., `google-play-scraper`, `python-dotenv`) and surfaces clear errors when a package is required.
- Data validation: `src/preprocessing.py` implements missing value handling, date normalization, duplicate removal, and a final data-quality report so you can measure KPI compliance (<5% missing critical fields).

KPIs (Task 1)
- Collect >=400 usable reviews per bank (aim 600 per bank as buffer).
- Final processed dataset with <5% missing critical fields.

Developer workflow
- Create a branch (`task-2`) for changes; commit frequently with descriptive messages.
- Push branch to origin and open a PR into `main` for review before merging.

Troubleshooting & tips
- If you see import errors for optional packages, install them:

```powershell
pip install -r requirements.txt
```

- If scraper fetches fewer reviews than expected, increase `reviews_per_bank` in `src/config.py` or verify the app availability on Google Play.

Next steps (Task 2)
- Add sentiment analysis (VADER or multilingual model) and topical modeling (LDA/NMF) notebooks.
- Add unit tests for `ReviewPreprocessor` and a minimal CI pipeline to run import/syntax checks on push.

Contact
- If you want, I can open a PR from `task-1` / `task-2` into `main` and add a GitHub Actions workflow to run basic checks on pushes.

