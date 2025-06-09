import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('../data/sentiment_reviews.csv')

# Example: Sentiment distribution bar chart
sentiment_counts = df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0)
sentiment_counts.plot(kind='bar', stacked=True)
plt.title('Sentiment Distribution by Bank')
plt.xlabel('Bank')
plt.ylabel('Count')
plt.savefig('../visualizations/sentiment_distribution.png')
plt.close()

print("Generated sentiment distribution plot")

# Commit guidance (manual step): git add task_4_visualizations.py; git commit -m "Add initial visualization script"; git push