-- CRUD Operation 1: INSERT
-- Insert Duke Tech university for 2014

INSERT INTO rankings (world_rank, institution, country, national_rank, quality_of_education, 
                      alumni_employment, quality_of_faculty, publications, influence, 
                      citations, broad_impact, patents, score, year)
VALUES (350, 'Duke Tech', 'USA', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 60.5, 2014);

-- Verify the insertion
SELECT * FROM rankings WHERE institution = 'Duke Tech' AND year = 2014;