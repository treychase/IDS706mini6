-- CRUD Operation 2: READ/QUERY
-- Count Japanese universities in global top 200 in 2013

SELECT COUNT(*) as japan_universities_top_200
FROM university_rankings
WHERE country = 'Japan' 
  AND year = 2013 
  AND CAST(world_rank AS INTEGER) <= 200;

-- Also show the actual universities for verification
SELECT institution, world_rank, score
FROM university_rankings
WHERE country = 'Japan' 
  AND year = 2013 
  AND CAST(world_rank AS INTEGER) <= 200
ORDER BY CAST(world_rank AS INTEGER);