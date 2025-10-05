-- CRUD Operation 4: DELETE
-- Delete universities with score below 45 in 2015

-- First, check how many records will be deleted
SELECT COUNT(*) as records_to_delete
FROM rankings
WHERE year = 2015 AND score < 45;

-- Show the records that will be deleted
SELECT institution, country, score
FROM rankings
WHERE year = 2015 AND score < 45;

-- Delete the records
DELETE FROM rankings
WHERE year = 2015 AND score < 45;

-- Verify deletion - should return 0 rows
SELECT COUNT(*) as remaining_low_scores
FROM rankings
WHERE year = 2015 AND score < 45;