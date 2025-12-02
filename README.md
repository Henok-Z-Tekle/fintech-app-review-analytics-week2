# Fintech App Review Analytics — Week 2 (Task 3: PostgreSQL Integration)

This module stores the cleaned and enriched review dataset (Task-1 + Task-2 outputs) into a PostgreSQL database.
The goal is to prepare a query-ready relational schema for downstream analytics (Task-4 dashboards & insights).

## Quick summary

Goal: Create a PostgreSQL database bank_reviews, store all banks & their reviews, and enable SQL-based analytics.

Inputs:

data/processed/reviews_processed.csv

data/processed/reviews_with_sentiment.csv (if Task 2 was completed)

Outputs:

PostgreSQL tables: banks, reviews

Records inserted: ~1200+ reviews (400 per bank)

Branching: Do your work on task-3, then open a Pull Request → main.

# Repository structure (Task-3 relevant)
src/
 ├── db_connection.py              # Reusable PostgreSQL connector
 ├── task3_postgres_setup.py       # Creates DB, tables, inserts data
 ├── task2_sentiment_thematic.py   # (Task 2 pipeline)
 ├── preprocessing.py              # (Task 1)
 └── config.py                     # DB + path configuration

data/
 ├── processed/
 │    ├── reviews_processed.csv
 │    └── reviews_with_sentiment.csv
 └── raw/

## PostgreSQL schema

Two tables are created:

1️⃣ banks
Column	Type	Notes
bank_id	SERIAL (PK)	Auto-generated
bank_code	VARCHAR	CBE, BOA, DASHEN
bank_name	TEXT	Full bank name
app_name	TEXT	App name on Play Store
2️⃣ reviews
Column	Type	Notes
review_id	TEXT (PK)	Unique Google Play ID
bank_id	INT (FK)	Linked to banks.bank_id
review_text	TEXT	Raw review text
rating	INT	1–5 stars
review_date	DATE	Normalized
sentiment_label	VARCHAR	POSITIVE / NEGATIVE
sentiment_score	REAL	Confidence (0–1)
source	TEXT	google_play
# Getting started (local, PowerShell)

Ensure PostgreSQL is running

Open:

SQL Shell (psql)


Login:

psql -U postgres


Enter password:

Henzi19$


Create the database manually (optional)

CREATE DATABASE bank_reviews;


If you do not create it manually, the Task-3 script will create it for you.

Run Task-3 pipeline

From project root:

python src/task3_postgres_setup.py


Expected output:

=== Task 3 – PostgreSQL Setup ===
[INFO] Database 'bank_reviews' already exists.
[INFO] Tables 'banks' and 'reviews' are ready.
[INFO] Inserted/updated banks metadata.
[INFO] Loading reviews from data/processed/reviews_with_sentiment.csv
[INFO] Inserting 1200 reviews...

[STATS] Review counts per bank:
('Bank of Abyssinia', 400, 3.2)
('Commercial Bank of Ethiopia', 400, 2.1)
('Dashen Bank', 400, 3.5)

[OK] Task 3 completed.

# Design & engineering notes

Idempotent design

Running Task-3 multiple times will not duplicate data.

Uses ON CONFLICT DO NOTHING for reviews.

Uses ON CONFLICT DO UPDATE for banks.

Automatic fallback

If reviews_with_sentiment.csv exists → uses it

Else → loads reviews_processed.csv & fills missing sentiment fields

Separation of concerns

db_connection.py handles DB connections

task3_postgres_setup.py handles creation & inserts

Queries and verification logic isolated cleanly

## KPIs (Task-3)

Database successfully created

banks table contains exactly 3 entries

reviews table contains ~1200+ entries

No review duplication

Sentiment columns preserved where available

Verification queries print accurate stats

## Developer workflow
git checkout -b task-3
git add .
git commit -m "Add Task 3: PostgreSQL integration (DB, tables, inserts)"
git push -u origin task-3


Open Pull Request → Merge into main.

## Troubleshooting & tips
psql: FATAL: password authentication failed

→ Ensure password is exactly:
Henzi19$

Script errors: cannot connect to localhost:5432

→ PostgreSQL service not running
Start it:

services.msc → postgresql-x64 → Start

pgAdmin not opening

→ Install from: https://www.pgadmin.org/download/

Next steps (Task 4)

Use SQL queries for:

Sentiment distribution per bank

Themes per bank

Rating averages

Negative vs positive review counts

Build visual dashboards:

matplotlib / seaborn notebooks

SQL-based aggregation views

Draft insights for final Week-2 report.
