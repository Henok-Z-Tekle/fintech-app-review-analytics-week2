# Fintech App Review Analytics — Week 2 (Task 2: Sentiment & Thematic Analysis)

This module extends the cleaned dataset from Task 1 by applying sentiment analysis, keyword extraction, and thematic clustering on user reviews collected from the Google Play Store for three major Ethiopian mobile banking apps. The objective for Week 2 (Task 2) is to generate an enriched, analysis-ready dataset that includes sentiment labels, confidence scores, cleaned text, keywords, and themes.

# Quick summary

Goal: Add sentiment labels, sentiment scores, cleaned text, TF-IDF keywords, and themes to the processed review dataset.

Input: data/processed/reviews_processed.csv (from Task 1)

Outputs:

data/processed/reviews_with_sentiment.csv

data/processed/keywords_per_bank.csv

Branching: Do development on task-2, then create a PR → main.

# Repository structure (Task-2 relevant)

src/

task2_sentiment_thematic.py — main Task-2 pipeline (sentiment, TF-IDF, themes)

preprocessing.py — used for Task-1 cleaning; now feeds Task-2

config.py — app IDs, paths, and pipeline configuration

notebooks/

task2_EDA.ipynb — exploratory notebook for sentiment/theme visualization

data/

processed/

reviews_processed.csv — cleaned dataset from Task-1

reviews_with_sentiment.csv — enriched output (Task-2)

keywords_per_bank.csv — TF-IDF outputs per bank

requirements.txt — project dependencies (Transformers, NLTK, Scikit-Learn)

# Getting started (local, PowerShell)

Activate venv & install dependencies:

cd 'C:\Users\heniz\OneDrive\Desktop\KAIM Files\fintech-app-review-analytics-week2'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt


⚠️ If you see missing NLTK resources (punkt, stopwords, wordnet), run:

import nltk
nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')


Ensure Task-1 output exists:

ls data/processed/reviews_processed.csv


If missing → run Task 1 first.

Run the Task-2 sentiment + thematic pipeline:

python src/task2_sentiment_thematic.py


Expected output:

[SUCCESS] Task 2 completed.
Reviews with sentiment → data/processed/reviews_with_sentiment.csv
Keywords per bank      → data/processed/keywords_per_bank.csv


Open the Task-2 notebook for visualization:

code notebooks/task2_EDA.ipynb

# Design & engineering notes

DistilBERT-based sentiment model
Uses distilbert-base-uncased-finetuned-sst-2-english.

Rule-based theme clustering
Theme dictionary includes:

Account Access Issues

Transaction Performance

App Stability & Bugs

Network & Connectivity

UI/UX

Customer Support

TF-IDF keyword extraction

Applied per bank

Extracts top 20 n-grams (1–2 gram tokens)

Pipeline structure
Task is modular:

Clean (clean_text)

Sentiment classifier

TF-IDF keywords

Theme tagging

Write enriched CSV outputs

# KPIs (Task-2)

100% of reviews assigned:

sentiment_label

sentiment_score

clean_text

themes

TF-IDF produces ranking of keywords for:

CBE Mobile Banking

BOA Mobile Banking

Dashen Bank SuperApp

Output files successfully written to:

data/processed/reviews_with_sentiment.csv
data/processed/keywords_per_bank.csv

# Developer workflow

Checkout a dedicated branch:

git checkout -b task-2


Stage, commit, push:

git add .
git commit -m "Add Task 2: Sentiment and Thematic Analysis pipeline"
git push -u origin task-2


Create a Pull Request → merge into main.

# Troubleshooting & tips

Transformers import failures
Install missing deps:

pip install transformers torch


NLTK errors
Run:

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


DistilBERT too slow?
Switch to a lighter sentiment model or truncate review text at 512 chars.

Next steps (Task 3)

Create PostgreSQL schema (reviews + apps tables).

Insert enriched Task-2 dataset into PostgreSQL.

Write SQL queries for:

sentiment distribution per bank

top negative keywords

theme frequency statistics

Use SQL-based EDA to support Task-4 insights.
