
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
