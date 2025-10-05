"""
Test file for database operations
"""

import sqlite3
import os
import shutil
import pytest
import sys
from io import StringIO


@pytest.fixture
def test_db():
    """Create a test database copy for testing"""
    # Create a backup of the original database
    if os.path.exists("university_database.db"):
        shutil.copy("university_database.db", "test_university_database.db")
        yield "test_university_database.db"
        # Cleanup: remove test database after tests
        if os.path.exists("test_university_database.db"):
            os.remove("test_university_database.db")
    else:
        pytest.skip("Original database file not found")


def test_database_exists():
    """Test that the database file exists"""
    assert os.path.exists(
        "university_database.db"
    ), "Database file university_database.db not found"


def test_database_connection(test_db):
    """Test database connection"""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    assert len(tables) > 0, "No tables found in database"


def test_rankings_table_exists(test_db):
    """Test that university_rankings table exists"""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='university_rankings';"
    )
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "university_rankings table not found"


def test_insert_operation(test_db):
    """Test INSERT operation - adding Duke Tech"""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    # Insert Duke Tech
    cursor.execute(
        """
        INSERT INTO university_rankings (world_rank, institution, country, score, year)
        VALUES (350, 'Duke Tech', 'USA', 60.5, 2014)
    """
    )
    conn.commit()

    # Verify insertion
    cursor.execute(
        "SELECT * FROM university_rankings WHERE institution='Duke Tech' AND year=2014"
    )
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Duke Tech was not inserted"
    assert result[2] == "USA", "Country should be USA"
    assert float(result[-2]) == 60.5, "Score should be 60.5"


def test_read_operation(test_db):
    """Test READ operation - count Japanese universities"""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) FROM university_rankings
        WHERE country = 'Japan' AND year = 2013 
        AND CAST(world_rank AS INTEGER) <= 200
    """
    )
    count = cursor.fetchone()[0]
    conn.close()

    assert count >= 0, "Count should be non-negative"
    assert isinstance(count, int), "Count should be an integer"


def test_update_operation(test_db):
    """Test UPDATE operation - increase Oxford score"""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    # Get original score
    cursor.execute(
        "SELECT score FROM university_rankings WHERE institution LIKE '%Oxford%' AND year = 2014"
    )
    result = cursor.fetchone()

    if result:
        original_score = float(result[0])

        # Update score
        cursor.execute(
            """
            UPDATE university_rankings SET score = score + 1.2
            WHERE institution LIKE '%Oxford%' AND year = 2014
        """
        )
        conn.commit()

        # Get updated score
        cursor.execute(
            "SELECT score FROM university_rankings WHERE institution LIKE '%Oxford%' AND year = 2014"
        )
        new_score = float(cursor.fetchone()[0])

        conn.close()

        assert (
            abs(new_score - (original_score + 1.2)) < 0.01
        ), "Score not updated correctly"
    else:
        conn.close()
        pytest.skip("Oxford not found in 2014 data")


def test_delete_operation(test_db):
    """Test DELETE operation - remove low scores"""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    # Count records before deletion
    cursor.execute(
        "SELECT COUNT(*) FROM university_rankings WHERE year = 2015 AND score < 45"
    )
    count_before = cursor.fetchone()[0]

    # Delete records
    cursor.execute("DELETE FROM university_rankings WHERE year = 2015 AND score < 45")
    conn.commit()

    # Count records after deletion
    cursor.execute(
        "SELECT COUNT(*) FROM university_rankings WHERE year = 2015 AND score < 45"
    )
    count_after = cursor.fetchone()[0]

    conn.close()

    assert count_after == 0, "Low score records should be deleted"


def test_basic_analysis_queries(test_db):
    """Test that basic analysis queries run without errors"""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    # Test total count
    cursor.execute("SELECT COUNT(*) FROM university_rankings")
    total = cursor.fetchone()[0]
    assert total > 0, "Database should have records"

    # Test grouping by year
    cursor.execute("SELECT year, COUNT(*) FROM university_rankings GROUP BY year")
    years = cursor.fetchall()
    assert len(years) > 0, "Should have records for multiple years"

    # Test average score calculation
    cursor.execute("SELECT AVG(score) FROM university_rankings")
    avg_score = cursor.fetchone()[0]
    assert avg_score is not None, "Should calculate average score"

    conn.close()


def test_sql_files_exist():
    """Test that all required SQL files exist"""
    required_files = [
        "connect.sql",
        "basic_analysis.sql",
        "insert.sql",
        "query_japan.sql",
        "update_oxford.sql",
        "delete_low_scores.sql",
    ]

    for file in required_files:
        assert os.path.exists(file), f"Required SQL file {file} not found"


def test_readme_exists():
    """Test that README.md exists"""
    assert os.path.exists("README.md"), "README.md not found"


def test_main_imports():
    """Test that main.py can be imported without errors"""
    try:
        import main

        assert hasattr(
            main, "run_analysis"
        ), "main.py should have run_analysis function"
        assert hasattr(
            main, "print_section"
        ), "main.py should have print_section function"
        assert hasattr(main, "print_table"), "main.py should have print_table function"
    except ImportError as e:
        pytest.fail(f"Failed to import main.py: {e}")


def test_print_section_function():
    """Test print_section function from main.py"""
    import main

    # Capture output
    captured_output = StringIO()
    sys.stdout = captured_output

    main.print_section("Test Section")

    # Reset stdout
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "Test Section" in output, "Section title should be in output"
    assert "=" in output, "Section should have separators"


def test_run_analysis_function():
    """Test that run_analysis function executes without errors"""
    import main

    # Capture output to prevent cluttering test output
    captured_output = StringIO()
    sys.stdout = captured_output

    try:
        main.run_analysis()
        success = True
    except Exception as e:
        success = False
        error = str(e)

    # Reset stdout
    sys.stdout = sys.__stdout__

    if not success:
        pytest.fail(f"run_analysis() failed with error: {error}")

    output = captured_output.getvalue()
    assert "ANALYSIS" in output.upper(), "Output should contain analysis results"
    assert "TOTAL RECORDS" in output.upper(), "Output should show total records"


def test_analysis_covers_all_sections():
    """Test that analysis includes all expected sections"""
    import main

    # Capture output
    captured_output = StringIO()
    sys.stdout = captured_output

    main.run_analysis()

    # Reset stdout
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue().upper()

    expected_sections = [
        "TOTAL RECORDS",
        "UNIVERSITIES BY YEAR",
        "SCORE STATISTICS",
        "TOP 10 UNIVERSITIES",
        "TOP 10 COUNTRIES",
        "SCORE DISTRIBUTION",
    ]

    for section in expected_sections:
        assert section in output, f"Analysis should include '{section}' section"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
