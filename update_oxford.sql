-- CRUD Operation 3: UPDATE
-- Update University of Oxford score in 2014 by adding 1.2 points

-- First, check the current score
SELECT institution, year, score 
FROM rankings 
WHERE institution LIKE '%Oxford%' AND year = 2014;

-- Update the score by adding 1.2
UPDATE rankings
SET score = score + 1.2
WHERE institution LIKE '%Oxford%' AND year = 2014;

-- Verify the update
SELECT institution, year, score 
FROM rankings 
WHERE institution LIKE '%Oxford%' AND year = 2014;