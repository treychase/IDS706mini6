"""
Display database analysis with nicely formatted output
"""

import sqlite3


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_table(cursor, max_rows=None):
    """Print query results as a formatted table"""
    results = cursor.fetchall()
    if not results:
        print("  No results found.")
        return

    # Get column names
    col_names = [description[0] for description in cursor.description]

    # Calculate column widths
    col_widths = [len(name) for name in col_names]
    for row in results[:max_rows] if max_rows else results:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Print header
    header = " | ".join(name.ljust(width) for name, width in zip(col_names, col_widths))
    print("  " + header)
    print("  " + "-" * len(header))

    # Print rows
    display_rows = results[:max_rows] if max_rows else results
    for row in display_rows:
        row_str = " | ".join(
            str(val).ljust(width) if val is not None else "NULL".ljust(width)
            for val, width in zip(row, col_widths)
        )
        print("  " + row_str)

    if max_rows and len(results) > max_rows:
        print(f"  ... and {len(results) - max_rows} more rows")

    print(f"\n  Total: {len(results)} row(s)")


def run_analysis():
    """Run comprehensive database analysis"""
    try:
        conn = sqlite3.connect("university_database.db")
        cursor = conn.cursor()

        print("\n" + "=" * 70)
        print("  UNIVERSITY RANKINGS DATABASE - COMPREHENSIVE ANALYSIS")
        print("=" * 70)

        # 1. Total Records
        print_section("1. TOTAL RECORDS")
        cursor.execute("SELECT COUNT(*) as total_records FROM university_rankings;")
        result = cursor.fetchone()
        print(f"  Total Records in Database: {result[0]:,}")

        # 2. Universities by Year
        print_section("2. UNIVERSITIES BY YEAR")
        cursor.execute(
            """
            SELECT year, COUNT(*) as university_count 
            FROM university_rankings 
            GROUP BY year 
            ORDER BY year;
        """
        )
        print_table(cursor)

        # 3. Score Statistics by Year
        print_section("3. SCORE STATISTICS BY YEAR")
        cursor.execute(
            """
            SELECT year, 
                   ROUND(AVG(score), 2) as avg_score,
                   ROUND(MIN(score), 2) as min_score,
                   ROUND(MAX(score), 2) as max_score
            FROM university_rankings 
            GROUP BY year 
            ORDER BY year;
        """
        )
        print_table(cursor)

        # 4. Top 10 Universities in 2015
        print_section("4. TOP 10 UNIVERSITIES BY SCORE (2015)")
        cursor.execute(
            """
            SELECT institution, country, world_rank, score 
            FROM university_rankings 
            WHERE year = 2015 
            ORDER BY score DESC 
            LIMIT 10;
        """
        )
        print_table(cursor)

        # 5. Top Countries
        print_section("5. TOP 10 COUNTRIES BY UNIVERSITY COUNT")
        cursor.execute(
            """
            SELECT country, COUNT(*) as university_count 
            FROM university_rankings 
            GROUP BY country 
            ORDER BY university_count DESC 
            LIMIT 10;
        """
        )
        print_table(cursor)

        # 6. Score Distribution
        print_section("6. SCORE DISTRIBUTION")
        cursor.execute(
            """
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
            FROM university_rankings
            GROUP BY score_range
            ORDER BY score_range DESC;
        """
        )
        print_table(cursor)

        # 7. Universities in All Years
        print_section("7. UNIVERSITIES APPEARING IN ALL YEARS (2012-2015)")
        cursor.execute(
            """
            SELECT institution, COUNT(DISTINCT year) as years_present
            FROM university_rankings
            GROUP BY institution
            HAVING COUNT(DISTINCT year) = 4
            LIMIT 10;
        """
        )
        print_table(cursor)

        # 8. USA Universities Analysis
        print_section("8. USA UNIVERSITIES ANALYSIS")
        cursor.execute(
            """
            SELECT 
                year,
                COUNT(*) as usa_universities,
                ROUND(AVG(score), 2) as avg_score,
                MAX(score) as max_score
            FROM university_rankings
            WHERE country = 'USA'
            GROUP BY year
            ORDER BY year;
        """
        )
        print_table(cursor)

        # 9. Top 5 Countries per Year
        print_section("9. TOP 5 COUNTRIES BY AVERAGE SCORE (2015)")
        cursor.execute(
            """
            SELECT 
                country,
                COUNT(*) as num_universities,
                ROUND(AVG(score), 2) as avg_score,
                MAX(score) as max_score
            FROM university_rankings
            WHERE year = 2015
            GROUP BY country
            HAVING COUNT(*) >= 5
            ORDER BY avg_score DESC
            LIMIT 5;
        """
        )
        print_table(cursor)

        # 10. World Rank Distribution
        print_section("10. TOP 100 vs REST COMPARISON")
        cursor.execute(
            """
            SELECT 
                CASE 
                    WHEN CAST(world_rank AS INTEGER) <= 100 THEN 'Top 100'
                    WHEN CAST(world_rank AS INTEGER) <= 200 THEN 'Top 101-200'
                    WHEN CAST(world_rank AS INTEGER) <= 300 THEN 'Top 201-300'
                    ELSE 'Below 300'
                END as rank_category,
                COUNT(*) as count,
                ROUND(AVG(score), 2) as avg_score
            FROM university_rankings
            WHERE year = 2015
            GROUP BY rank_category
            ORDER BY avg_score DESC;
        """
        )
        print_table(cursor)

        conn.close()

        print("\n" + "=" * 70)
        print("  ANALYSIS COMPLETE")
        print("=" * 70 + "\n")

    except sqlite3.Error as e:
        print(f"\n✗ Database error: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    run_analysis()
