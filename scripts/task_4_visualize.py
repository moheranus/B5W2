import pandas as pd
import psycopg2
import os
import matplotlib.pyplot as plt

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
    SELECT bank_id, sentiment_score, themes
    FROM Reviews
    WHERE sentiment_score IS NOT NULL
"""
df = pd.read_sql(query, connection)

# Close connection
cursor.close()
connection.close()

# Save to CSV
df.to_csv('../data/processed/visualization_data.csv', index=False)
print("Data extracted and saved to data/processed/visualization_data.csv")

# Sentiment trend by bank
sentiment_by_bank = df.groupby('bank_id')['sentiment_score'].mean()
sentiment_by_bank.plot(kind='bar', title='Average Sentiment Score by Bank')
plt.ylabel('Sentiment Score')
os.makedirs('../visualizations', exist_ok=True)
plt.savefig('../visualizations/sentiment_trend.png')
plt.close()

# Theme distribution
theme_counts = df['themes'].value_counts()
theme_counts.plot(kind='pie', title='Theme Distribution', autopct='%1.1f%%')
plt.ylabel('')  # Hide y-label for pie
plt.savefig('../visualizations/theme_distribution.png')
plt.close()

print("Visualizations saved to visualizations/ directory")