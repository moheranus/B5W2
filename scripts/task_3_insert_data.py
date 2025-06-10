import pandas as pd
import psycopg2
import os

# Connect to PostgreSQL (update with your credentials)
connection = psycopg2.connect(
    dbname="bank_reviews",
    user="postgres",
    password="Password.01", 
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

# Load processed data
df = pd.read_csv('../data/processed/sentiment_reviews.csv')

# Insert data into Reviews table
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO Reviews (bank_id, review_text, rating, date_posted, source, sentiment_label, sentiment_score, themes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['bank'], row['review'], row['rating'], row['date'], row['source'], row['sentiment_label'], row['sentiment_score'], row['themes']))

# Commit and close
connection.commit()
cursor.close()
connection.close()
print("Data inserted into PostgreSQL database.")