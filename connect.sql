-- Connect to the database and verify tables exist
-- List all tables in the database
SELECT name FROM sqlite_master WHERE type='table';

-- Show schema for university_rankings table
PRAGMA table_info(university_rankings);

-- Display first 5 rows to verify connection
SELECT * FROM university_rankings LIMIT 5;