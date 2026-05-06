# Step 5: SQL Analysis

import pandas as pd
import sqlite3

# Load cleaned data
df = pd.read_csv('netflix_cleaned.csv')

# Create SQL database in memory
conn = sqlite3.connect('netflix.db')
df.to_sql('netflix', conn, if_exists='replace', index=False)

print("=== DATABASE CREATED ===")
print("Running SQL queries on Netflix data...\n")

# ---- QUERY 1: Total Movies vs TV Shows ----
q1 = pd.read_sql_query("""
    SELECT type, COUNT(*) as total
    FROM netflix
    GROUP BY type
    ORDER BY total DESC
""", conn)
print("=== Q1: Movies vs TV Shows ===")
print(q1)

# ---- QUERY 2: Top 10 Countries ----
q2 = pd.read_sql_query("""
    SELECT country, COUNT(*) as total
    FROM netflix
    WHERE country != 'Unknown'
    GROUP BY country
    ORDER BY total DESC
    LIMIT 10
""", conn)
print("\n=== Q2: Top 10 Countries ===")
print(q2)

# ---- QUERY 3: Content added per year ----
q3 = pd.read_sql_query("""
    SELECT year_added, COUNT(*) as total
    FROM netflix
    WHERE year_added IS NOT NULL
    GROUP BY year_added
    ORDER BY year_added
""", conn)
print("\n=== Q3: Content Added Per Year ===")
print(q3)

# ---- QUERY 4: Top 10 Ratings ----
q4 = pd.read_sql_query("""
    SELECT rating, COUNT(*) as total
    FROM netflix
    GROUP BY rating
    ORDER BY total DESC
    LIMIT 10
""", conn)
print("\n=== Q4: Top Ratings ===")
print(q4)

# ---- QUERY 5: Movies added after 2016 ----
q5 = pd.read_sql_query("""
    SELECT type, COUNT(*) as total
    FROM netflix
    WHERE year_added >= 2016
    GROUP BY type
""", conn)
print("\n=== Q5: Content Added After 2016 ===")
print(q5)

# ---- QUERY 6: Top Directors ----
q6 = pd.read_sql_query("""
    SELECT director, COUNT(*) as total
    FROM netflix
    WHERE director != 'Unknown'
    GROUP BY director
    ORDER BY total DESC
    LIMIT 10
""", conn)
print("\n=== Q6: Top 10 Directors ===")
print(q6)

# Save SQL queries to file
sql_queries = """
-- Netflix SQL Analysis
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

import os
os.makedirs('sql', exist_ok=True)
with open('sql/netflix_queries.sql', 'w') as f:
    f.write(sql_queries)

conn.close()
print("\n✅ SQL database created: netflix.db")
print("✅ SQL queries saved: sql/netflix_queries.sql")
print("\n🎉 SQL Analysis Complete!")
