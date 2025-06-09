from transformers import pipeline
import pandas as pd

# Load preprocessed data
df = pd.read_csv('../data/raw_reviews.csv')

# Sentiment analysis with DistilBERT
sentiment_analyzer = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

def get_sentiment(text):
    try:
        result = sentiment_analyzer(text[:512])[0]  # Truncate to 512 tokens
        return result['label'], result['score']
    except Exception as e:
        return 'neutral', 0.0

# Apply sentiment analysis (limit to 400+ reviews for now)
df = df.head(400)  # Temporary limit for speed, remove later
df['sentiment_label'], df['sentiment_score'] = zip(*df['review'].apply(get_sentiment))

# Save results
df.to_csv('../data/sentiment_reviews.csv', index=False)
print(f"Processed sentiment for {len(df)} reviews. Saved to data/sentiment_reviews.csv")

# Thematic analysis (skeleton - expand later)
# Example keyword extraction (to be completed)
# import spacy
# nlp = spacy.load('en_core_web_sm')
# df['keywords'] = df['review'].apply(lambda x: [token.text for token in nlp(x) if token.is_alpha and not token.is_stop])

# Commit guidance (manual step): git add task_2_sentiment_themes.py; git commit -m "Add initial sentiment analysis with DistilBERT"; git push