from google_play_scraper import reviews_all, Sort
import pandas as pd
from datetime import datetime

# Define app IDs 
apps = {
    'CBE': 'com.combanketh.mobilebanking',    
    'BOA': 'com.boa.boaMobileBanking',    
    'Dashen': 'com.dashen.dashensuperapp'  
}

all_reviews = []
for bank, app_id in apps.items():
    print(f"Scraping reviews for {bank} ({app_id})...")
    try:
        result = reviews_all(
            app_id,
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=400  # Target minimum 400 reviews per bank
        )
        for review in result:
            all_reviews.append({
                'bank': bank,
                'review': review['content'],
                'rating': review['score'],
                'date': review['at'].strftime('%Y-%m-%d'),
                'source': 'Google Play'
            })
    except Exception as e:
        print(f"Error scraping {bank}: {e}")

# Convert to DataFrame
df = pd.DataFrame(all_reviews)

# Preprocessing
# Remove duplicates
df = df.drop_duplicates(subset=['review', 'bank'], keep='first')

# Handle missing data
df = df.dropna(subset=['review'])

# Normalize dates
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Save to CSV
df.to_csv('../data/raw_reviews.csv', index=False)
print(f"Scraped and preprocessed {len(df)} reviews. Saved to data/raw_reviews.csv")

# Commit guidance (manual step): git add task_1_scrape_preprocess.py; git commit -m "Add scraping and preprocessing for 1200+ reviews"; git push