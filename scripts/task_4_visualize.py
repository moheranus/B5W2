import pandas as pd
import psycopg2
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to PostgreSQL
connection = psycopg2.connect(
    dbname="bank_reviews",
    user="postgres",
    password="Password.01",  
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

# Query data
query = """
    SELECT bank_id, sentiment_score, rating, themes
    FROM Reviews
    WHERE sentiment_score IS NOT NULL AND rating IS NOT NULL
"""
df = pd.read_sql(query, connection)

# Close connection
cursor.close()
connection.close()

# Save to CSV
df.to_csv('../data/processed/visualization_data.csv', index=False)
print("Data extracted and saved to data/processed/visualization_data.csv")

# Insights: Drivers and Pain Points
drivers = {}
pain_points = {}
for bank in df['bank_id'].unique():
    bank_df = df[df['bank_id'] == bank]
    avg_sentiment = bank_df['sentiment_score'].mean()
    themes = bank_df['themes'].value_counts()
    # Drivers: High sentiment with common themes
    if avg_sentiment > 0.95:
        drivers[bank] = [theme for theme in themes.index if themes[theme] > 50 and theme != 'Other'][:2] or ['User Interface']
    else:
        drivers[bank] = ['User Interface']  # Default driver
    # Pain Points: Low sentiment with common themes
    if avg_sentiment < 0.97:
        pain_points[bank] = [theme for theme in themes.index if themes[theme] > 50 and theme != 'Other'][:2] or ['Reliability Issues']
    else:
        pain_points[bank] = ['Reliability Issues']  # Default pain point

print("Drivers:", drivers)
print("Pain Points:", pain_points)

# Comparison: Average Sentiment by Bank
sentiment_by_bank = df.groupby('bank_id')['sentiment_score'].mean()
print("Sentiment Comparison:", sentiment_by_bank)

# Recommendations
recommendations = {
    'CBE': ['Add a budgeting tool to enhance user experience', 'Improve crash reporting'],
    'BOA': ['Optimize app performance for faster load times', 'Enhance UI design'],
    'Dashen': ['Implement real-time support chat', 'Fix reliability issues']
}
print("Recommendations:", recommendations)

# Visualizations
os.makedirs('../visualizations', exist_ok=True)

# 1. Sentiment Trend by Bank (Bar Chart)
plt.figure(figsize=(10, 6))
sentiment_by_bank.plot(kind='bar', color='skyblue')
plt.title('Average Sentiment Score by Bank')
plt.xlabel('Bank')
plt.ylabel('Sentiment Score')
plt.savefig('../visualizations/sentiment_trend.png')
plt.close()

# 2. Rating Distribution (Histogram)
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='rating', hue='bank_id', multiple='stack')
plt.title('Rating Distribution by Bank')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.savefig('../visualizations/rating_distribution.png')
plt.close()

# 3. Theme Distribution (Pie Chart)
theme_counts = df['themes'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(theme_counts, labels=theme_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Theme Distribution Across Reviews')
plt.savefig('../visualizations/theme_distribution.png')
plt.close()

print("Visualizations saved to visualizations/ directory")