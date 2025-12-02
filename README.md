# Task 4 — Insights & Recommendations (Week 2)

Task 4 transforms the cleaned + enriched dataset (Task 1 & Task 2) into actionable insights through visualizations and evidence-based recommendations. The goal is to understand customer satisfaction drivers, pain points, and opportunities for improvement across Ethiopian fintech apps.

## Quick Summary

Inputs:

data/processed/reviews_with_sentiment.csv

data/processed/keywords_per_bank.csv

Outputs:

3–5 visualizations (figures/)

Drivers & pain points per bank

Practical improvement recommendations

Branching: Work on task-4, open PR → main.

# Repository Structure (Task-4 Relevant)
src/
 ├── task4_insights_visualization.py     # Generates Task 4 plots
 ├── task2_sentiment_thematic.py         # Provides sentiment + themes
 ├── preprocessing.py                    # Task 1 data preparation
 ├── db_connection.py                    # Task 3
 └── config.py                           # Paths & DB config

figures/
 ├── rating_distribution_per_bank.png
 ├── sentiment_distribution_per_bank.png
 ├── themes_per_bank.png
 └── top_keywords_per_bank.png

# How to Run Task-4

Ensure Task-2 & Task-3 outputs exist:

data/processed/reviews_with_sentiment.csv
data/processed/keywords_per_bank.csv


Run Task-4 script:

python src/task4_insights_visualization.py


Open figures/ directory for visual outputs.

Insights Extracted (Example Structure)

(These will be automatically computed; interpretation happens in final report)

Positive Drivers

Fast login, good navigation

Smooth transactions

Clean UI

Pain Points

Frequent crashes

Login failures

Slow transfer performance

Bank Comparison Example

Dashen Bank → Better UI & performance sentiment

CBE → Higher complaints about system downtime

BOA → Balanced reviews but more login-related issues

# KPIs

2+ drivers & 2+ pain points per bank

3–5 labeled visualizations

Clear, evidence-backed recommendations

# Developer Workflow
git checkout -b task-4
git add .
git commit -m "Add Task 4 insights and visualizations"
git push -u origin task-4
# Then open PR to main
