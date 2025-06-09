import cx_Oracle
import pandas as pd

# Connect to Oracle (update with your credentials)
connection = cx_Oracle.connect(user='your_user', password='your_password', dsn='localhost/XE')
cursor = connection.cursor()

# Load processed data
df = pd.read_csv('../data/sentiment_reviews.csv')

# Insert banks (manual setup, update with actual IDs)
banks = [('CBE', 'com.cbe.mobile'), ('BOA', 'com.boa.mobile'), ('Dashen', 'com.dashen.mobile')]
cursor.executemany("INSERT INTO Banks (bank_id, bank_name, app_id) VALUES (:1, :2, :3)",
                   [(i+1, name, app_id) for i, (name, app_id) in enumerate(banks)])

# Insert reviews
reviews = [(i+1, row['bank'], row['review'], row['rating'], row['date'], row['source'],
            row['sentiment_label'], row['sentiment_score'], '')  # Themes empty for now
           for i, row in df.iterrows()]
cursor.executemany("INSERT INTO Reviews (review_id, bank_id, review_text, rating, date, source, sentiment_label, sentiment_score, themes) "
                   "VALUES (:1, (SELECT bank_id FROM Banks WHERE bank_name=:2), :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6, :7, :8, :9)",
                   reviews)

# Commit and close
connection.commit()
cursor.close()
connection.close()
print(f"Inserted {len(df)} reviews into Oracle database")

# Commit guidance (manual step): git add task_3_insert_data.py; git commit -m "Add Oracle data insertion script"; git push