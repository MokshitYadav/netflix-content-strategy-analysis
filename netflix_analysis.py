# Netflix Content Strategy & Trend Analysis
# By Mokshit Yadav
# Tools: Python, SQL, Scikit-Learn, Power BI


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import sqlite3
import os


#LOAD & EXPLORE DATASET


df = pd.read_csv('netflix_titles.csv')

print("=" * 50)
print("STEP 1: DATASET OVERVIEW")
print("=" * 50)
print(f"Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nMissing Values:\n{df.isnull().sum()}")

#DATA CLEANING


print("\n" + "=" * 50)
print("STEP 2: DATA CLEANING")
print("=" * 50)

df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Not Rated')
df['duration'] = df['duration'].fillna('Unknown')

# Convert date_added to datetime
df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

# Remove duplicates
df.drop_duplicates(inplace=True)

print(f"Total rows after cleaning: {len(df)}")
print(f"Missing values after cleaning:\n{df.isnull().sum()}")

# Save cleaned data
df.to_csv('netflix_cleaned.csv', index=False)
print("✅ Cleaned data saved as netflix_cleaned.csv")


#EXPLORATORY DATA ANALYSIS (EDA)


print("\n" + "=" * 50)
print("STEP 3: EDA - CREATING CHARTS")
print("=" * 50)

os.makedirs('charts', exist_ok=True)
sns.set_style('darkgrid')
plt.rcParams['figure.figsize'] = (10, 6)

# Chart 1: Movies vs TV Shows
plt.figure()
df['type'].value_counts().plot(kind='bar', color=['#E50914', '#221F1F'])
plt.title('Movies vs TV Shows on Netflix')
plt.xlabel('Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('charts/01_movies_vs_tvshows.png')
plt.close()
print("✅ Chart 1 saved: Movies vs TV Shows")

# Chart 2: Top 10 Countries
plt.figure()
top_countries = df[df['country'] != 'Unknown']['country'].value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index, hue=top_countries.index, palette='Reds_r', legend=False)
plt.title('Top 10 Countries on Netflix')
plt.xlabel('Number of Titles')
plt.tight_layout()
plt.savefig('charts/02_top_countries.png')
plt.close()
print("✅ Chart 2 saved: Top 10 Countries")

# Chart 3: Content Added Per Year
plt.figure()
yearly = df['year_added'].value_counts().sort_index()
sns.lineplot(x=yearly.index, y=yearly.values, color='#E50914', linewidth=2.5)
plt.title('Content Added to Netflix Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Titles')
plt.tight_layout()
plt.savefig('charts/03_content_per_year.png')
plt.close()
print("✅ Chart 3 saved: Content Per Year")

# Chart 4: Top 10 Genres
plt.figure()
genres = df['listed_in'].str.split(',').explode().str.strip()
top_genres = genres.value_counts().head(10)
sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index, palette='Reds_r', legend=False)
plt.title('Top 10 Genres on Netflix')
plt.xlabel('Count')
plt.tight_layout()
plt.savefig('charts/04_top_genres.png')
plt.close()
print("✅ Chart 4 saved: Top 10 Genres")

# Chart 5: Ratings Distribution
plt.figure()
df['rating'].value_counts().plot(kind='bar', color='#E50914')
plt.title('Content Rating Distribution')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('charts/05_ratings.png')
plt.close()
print("✅ Chart 5 saved: Ratings Distribution")

print("\n🎉 All 5 EDA charts saved in charts/ folder!")


#K-MEANS CLUSTERING ML MODEL


print("\n" + "=" * 50)
print("STEP 4: K-MEANS CLUSTERING MODEL")
print("=" * 50)

df_clean = pd.read_csv('netflix_cleaned.csv')

df_clean['type_encoded'] = df_clean['type'].map({'Movie': 1, 'TV Show': 0})
df_clean['duration_mins'] = df_clean['duration'].str.extract(r'(\d+)').astype(float)

features = df_clean[['type_encoded', 'release_year', 'duration_mins']].dropna()

scaler = StandardScaler()
scaled = scaler.fit_transform(features)

print(f"Training K-Means on {len(features)} Netflix titles...")

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans.fit(scaled)

features = features.copy()
features['cluster'] = kmeans.labels_

print(f"✅ Model built successfully!")
print(f"\nCluster Distribution:\n{features['cluster'].value_counts().sort_index()}")

# Cluster visualization
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    features['release_year'],
    features['duration_mins'],
    c=features['cluster'],
    cmap='Set1',
    alpha=0.5,
    s=10
)
plt.colorbar(scatter, label='Cluster')
plt.title('Netflix Content Clusters (K-Means)')
plt.xlabel('Release Year')
plt.ylabel('Duration (mins/episodes)')
plt.tight_layout()
plt.savefig('charts/06_kmeans_clusters.png')
plt.close()
print("✅ Cluster chart saved!")

# Save clustered data
df_result = df_clean.copy()
df_result = df_result.iloc[features.index]
df_result['cluster'] = features['cluster'].values
df_result.to_csv('netflix_clustered.csv', index=False)
print("✅ Clustered data saved as netflix_clustered.csv")

# Cluster Summary
print("\nCluster Summary:")
summary = df_result.groupby('cluster').agg({
    'type': lambda x: x.value_counts().index[0],
    'release_year': 'mean',
    'duration_mins': 'mean',
    'title': 'count'
}).rename(columns={'title': 'total_titles'})
print(summary)


#SQL ANALYSIS


print("\n" + "=" * 50)
print("STEP 5: SQL ANALYSIS")
print("=" * 50)

df_sql = pd.read_csv('netflix_cleaned.csv')
conn = sqlite3.connect('netflix.db')
df_sql.to_sql('netflix', conn, if_exists='replace', index=False)

print("Database created! Running queries...\n")

q1 = pd.read_sql_query("SELECT type, COUNT(*) as total FROM netflix GROUP BY type ORDER BY total DESC", conn)
print("Q1: Movies vs TV Shows")
print(q1)

q2 = pd.read_sql_query("SELECT country, COUNT(*) as total FROM netflix WHERE country != 'Unknown' GROUP BY country ORDER BY total DESC LIMIT 10", conn)
print("\nQ2: Top 10 Countries")
print(q2)

q3 = pd.read_sql_query("SELECT year_added, COUNT(*) as total FROM netflix WHERE year_added IS NOT NULL GROUP BY year_added ORDER BY year_added", conn)
print("\nQ3: Content Added Per Year")
print(q3)

q4 = pd.read_sql_query("SELECT rating, COUNT(*) as total FROM netflix GROUP BY rating ORDER BY total DESC LIMIT 10", conn)
print("\nQ4: Top Ratings")
print(q4)

q5 = pd.read_sql_query("SELECT type, COUNT(*) as total FROM netflix WHERE year_added >= 2016 GROUP BY type", conn)
print("\nQ5: Content Added After 2016")
print(q5)

q6 = pd.read_sql_query("SELECT director, COUNT(*) as total FROM netflix WHERE director != 'Unknown' GROUP BY director ORDER BY total DESC LIMIT 10", conn)
print("\nQ6: Top 10 Directors")
print(q6)

# Save SQL file
os.makedirs('sql', exist_ok=True)
sql_queries = """-- Netflix SQL Analysis
-- By Mokshit Yadav

-- Q1: Movies vs TV Shows
SELECT type, COUNT(*) as total
FROM netflix
GROUP BY type
ORDER BY total DESC;

-- Q2: Top 10 Countries
SELECT country, COUNT(*) as total
FROM netflix
WHERE country != 'Unknown'
GROUP BY country
ORDER BY total DESC
LIMIT 10;

-- Q3: Content Added Per Year
SELECT year_added, COUNT(*) as total
FROM netflix
WHERE year_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added;

-- Q4: Top Ratings
SELECT rating, COUNT(*) as total
FROM netflix
GROUP BY rating
ORDER BY total DESC
LIMIT 10;

-- Q5: Content After 2016
SELECT type, COUNT(*) as total
FROM netflix
WHERE year_added >= 2016
GROUP BY type;

-- Q6: Top 10 Directors
SELECT director, COUNT(*) as total
FROM netflix
WHERE director != 'Unknown'
GROUP BY director
ORDER BY total DESC
LIMIT 10;
"""

with open('sql/netflix_queries.sql', 'w') as f:
    f.write(sql_queries)

conn.close()
print("\n✅ SQL database saved: netflix.db")
print("✅ SQL queries saved: sql/netflix_queries.sql")

print("\n" + "=" * 50)
print("COMPLETED")
print("=" * 50)
print("Files created:")
print("  ✅ netflix_cleaned.csv")
print("  ✅ netflix_clustered.csv")
print("  ✅ charts/ (6 PNG files)")
print("  ✅ sql/netflix_queries.sql")
print("  ✅ netflix.db")
