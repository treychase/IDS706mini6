-- Basic Analysis Queries for University Rankings Database

-- 1. Count total number of records
SELECT COUNT(*) as total_records FROM rankings;

-- 2. Count universities by year
SELECT year, COUNT(*) as university_count 
FROM rankings 
GROUP BY year 
ORDER BY year;

-- 3. Average score by year
SELECT year, 
       ROUND(AVG(score), 2) as avg_score,
       ROUND(MIN(score), 2) as min_score,
       ROUND(MAX(score), 2) as max_score
FROM rankings 
GROUP BY year 
ORDER BY year;

-- 4. Top 10 universities by score in 2015
SELECT institution, country, world_rank, score 
FROM rankings 
WHERE year = 2015 
ORDER BY score DESC 
LIMIT 10;

-- 5. Count universities by country (top 10 countries)
SELECT country, COUNT(*) as university_count 
FROM rankings 
GROUP BY country 
ORDER BY university_count DESC 
LIMIT 10;

-- 6. Distribution of scores (score ranges)
SELECT 
    CASE 
        WHEN score >= 90 THEN '90-100'
        WHEN score >= 80 THEN '80-89'
        WHEN score >= 70 THEN '70-79'
        WHEN score >= 60 THEN '60-69'
        WHEN score >= 50 THEN '50-59'
        ELSE 'Below 50'
    END as score_range,
    COUNT(*) as count
FROM rankings
GROUP BY score_range
ORDER BY score_range DESC;

-- 7. Universities that appear in all years (2012-2015)
SELECT institution, COUNT(DISTINCT year) as years_present
FROM rankings
GROUP BY institution
HAVING COUNT(DISTINCT year) = 4
LIMIT 10;