# Fintech App Review Analytics — Full Project (Tasks 1–4)

10 Academy · AI Mastery · Week 2 Project
Author: Henok Zenebe Tekle
Email: henok.z.tekle@gmail.com

This repository contains the complete workflow for analyzing customer feedback of Ethiopian mobile banking apps—CBE, Bank of Abyssinia, and Dashen Bank—using scraping, NLP, PostgreSQL, and data visualization.

📌 Project Goals

Scrape real reviews from the Google Play Store

Clean & structure the dataset

Apply NLP techniques (sentiment + themes)

Store data in PostgreSQL

Generate insights & recommendations

Produce clear, reproducible analytics workflow

# 📁 Repository Structure
src/
 ├── scraper.py
 ├── preprocessing.py
 ├── preprocessing_EDA.ipynb
 ├── task2_sentiment_thematic.py
 ├── task3_postgres_setup.py
 ├── task4_insights_visualization.py
 ├── db_connection.py
 └── config.py

scripts/
 ├── scrape_reviews.py
 └── preprocess.py

data/
 ├── raw/
 └── processed/
       ├── reviews_clean.csv
       ├── reviews_processed.csv
       ├── reviews_with_sentiment.csv
       ├── keywords_per_bank.csv

figures/
 ├── rating_distribution_per_bank.png
 ├── sentiment_distribution_per_bank.png
 ├── themes_per_bank.png
 └── top_keywords_per_bank.png

README.md
requirements.txt
.gitignore

# 🧾 Task Breakdown
## Task 1 — Data Collection & Preprocessing

What was done:

Scraped 400–600 reviews per bank using Google Play Scraper

Cleaned text, removed duplicates, normalized dates

Exported clean dataset:

review_text, rating, review_date, bank_code, bank_name, source

KPI achieved: > 1,200 clean reviews

## Task 2 — Sentiment & Thematic Analysis

Used DistilBERT for sentiment scoring

Labeled reviews as POSITIVE or NEGATIVE

Extracted keywords & themes using:

TF-IDF

spaCy NLP pipeline

Saved enriched dataset:

reviews_with_sentiment.csv

keywords_per_bank.csv

## Task 3 — PostgreSQL Database Integration

Created database: bank_reviews

Tables:

banks

reviews

Inserted > 1,200 reviews via Python (psycopg2)

Verified:

review counts

sentiment distribution

duplicates = 0

## Task 4 — Insights & Recommendations

Generated 4 visualizations:

Rating distribution

Sentiment distribution

Theme frequencies

Keyword importance

Identified:

Top drivers

Top pain points

Suggested improvements per bank

Prepared content for final 4-page report

# 🚀 How to Run the Full Pipeline
1. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

2. Scrape reviews (Task 1)
python scripts/scrape_reviews.py

3. Preprocess dataset
python scripts/preprocess.py

4. Generate sentiment & themes (Task 2)
python src/task2_sentiment_thematic.py

5. Import into PostgreSQL (Task 3)
python src/task3_postgres_setup.py

6. Generate visualizations (Task 4)
python src/task4_insights_visualization.py

## 📌 Key KPIs Achieved

✔ 1,200+ reviews

✔ Clean dataset with <5% missing data

✔ DistilBERT sentiment analysis

✔ PostgreSQL database with 2 tables

✔ 4 meaningful visualizations

✔ Insights ready for final report

📞 Contact

Name: Henok Zenebe Tekle
Email: henok.z.tekle@gmail.com
