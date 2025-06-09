from transformers import pipeline
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import torch

# Load cleaned data
df = pd.read_csv('../data/raw_reviews.csv')

# Sentiment Analysis with DistilBERT (CPU mode)
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def get_sentiment(text):
    try:
        result = sentiment_analyzer(text)[0]
        return result['label'], result['score']
    except Exception as e:
        return 'neutral', 0.5  # Fallback for errors

# Apply sentiment analysis (batch processing)
batch_size = 32
sentiments = []
for i in range(0, len(df), batch_size):
    batch = df['review'][i:i + batch_size].tolist()
    batch_sentiments = sentiment_analyzer(batch)
    for res in batch_sentiments:
        sentiments.append((res['label'], res['score']))

df['sentiment_label'], df['sentiment_score'] = zip(*sentiments)

# Aggregate sentiment by bank and rating
sentiment_summary = df.groupby(['bank', 'rating']).agg({'sentiment_score': 'mean'}).reset_index()
print("Sentiment Summary:\n", sentiment_summary)

# Thematic Analysis - Keyword Extraction with TF-IDF
tfidf = TfidfVectorizer(max_features=10, stop_words='english')
all_keywords = []
for bank in df['bank'].unique():
    bank_reviews = df[df['bank'] == bank]['review']
    tfidf_matrix = tfidf.fit_transform(bank_reviews)
    feature_names = tfidf.get_feature_names_out()
    tfidf_scores = tfidf_matrix.sum(axis=0).A1
    keywords = [(feature_names[i], tfidf_scores[i]) for i in tfidf_scores.argsort()[::-1][:5]]
    all_keywords.append({'bank': bank, 'keywords': keywords})
    print(f"Top keywords for {bank}: {keywords}")

# Manual theme clustering (example logic)
themes = {}
for item in all_keywords:
    bank = item['bank']
    themes[bank] = []
    for keyword, _ in item['keywords']:
        if any(x in keyword for x in ['crash', 'bug', 'error']):
            themes[bank].append('Reliability Issues')
        elif any(x in keyword for x in ['ui', 'design', 'interface']):
            themes[bank].append('User Interface')
        elif any(x in keyword for x in ['speed', 'slow', 'fast']):
            themes[bank].append('Performance')
        else:
            themes[bank].append('Other')

# Add themes to DataFrame
df['themes'] = df['bank'].map(lambda x: themes.get(x, ['Other'])[0])

# Save results
os.makedirs('../data/processed', exist_ok=True)
df.to_csv('../data/processed/sentiment_reviews.csv', index=False)
print(f"Saved sentiment and theme analysis to data/processed/sentiment_reviews.csv")