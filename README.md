Customer Experience Analytics for Ethiopian Banking Apps

Overview

This repository contains code and documentation for the B5W2 challenge, analyzing Google Play Store reviews for three Ethiopian banks: Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank. The project involves web scraping, sentiment and thematic analysis, Oracle database storage, and visualization to provide actionable insights.

Setup Instructions





Clone the repository: git clone [<repository-url>](https://github.com/moheranus/B5W2.git)



Install dependencies: pip install -r requirements.txt



Download spaCy model: python -m spacy download en_core_web_sm



Configure Oracle XE (see Oracle Setup section).

Project Structure





task_1_scrape_preprocess.py: Scrapes and preprocesses reviews.



task_2_sentiment_themes.py: Performs sentiment and thematic analysis.



task_3_oracle_setup.sql: Defines Oracle database schema.



task_3_insert_data.py: Inserts data into Oracle.



task_4_visualizations.py: Generates visualizations.



bank_reviews.csv: Cleaned review data.



bank_reviews_analyzed.csv: Analyzed review data.



final_report.md: Final report with insights.

Methodology





Scraping: Use google-play-scraper to collect 400+ reviews per bank.



Preprocessing: Remove duplicates, normalize dates, save as CSV.



Sentiment Analysis: Apply VADER for sentiment scoring.



Thematic Analysis: Use TF-IDF and manual clustering for themes.



Database: Store data in Oracle XE (Banks, Reviews tables).



Visualization: Create plots with Matplotlib/Seaborn.

Git Workflow





Create branches: git checkout -b task-<number>



Commit frequently: git commit -m "Descriptive message"



Push: git push origin task-<number>



Merge via pull requests on GitHub.