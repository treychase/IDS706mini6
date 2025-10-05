"""
Verify that all SQL files work with the correct table name
"""

import sqlite3
import os


def test_sql_file(filename, description):
    """Test a single SQL file"""
    print(f"\n{'='*60}")
    print(f"Testing: {filename}")
    print(f"Description: {description}")
    print(f"{'='*60}")

    if not os.path.exists(filename):
        print(f"   ✗ File not found: {filename}")
        return False

    try:
        conn = sqlite3.connect("university_database.db")
        cursor = conn.cursor()

        with open(filename, "r") as f:
            sql_script = f.read()

        # Split by semicolon and execute
        statements = sql_script.split(";")
        for i, statement in enumerate(statements):
            statement = statement.strip()
            if statement and not statement.startswith("--"):
                try:
                    cursor.execute(statement)
                    if statement.upper().strip().startswith("SELECT"):
                        results = cursor.fetchall()
                        if results:
                            print(f"   ✓ Query {i+1}: Returned {len(results)} rows")
                            # Show first result
                            if len(results[0]) <= 5:
                                print(f"      First result: {results[0]}")
                    else:
                        print(f"   ✓ Statement {i+1}: Executed successfully")
                        conn.commit()
                except sqlite3.Error as e:
                    print(f"   ✗ Error in statement {i+1}: {e}")
                    print(f"      Statement: {statement[:100]}...")
                    conn.rollback()
                    return False

        conn.close()
        print(f"   ✓✓✓ {filename} - ALL TESTS PASSED ✓✓✓")
        return True

    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False


def main():
    print("=" * 60)
    print("SQL FILES VERIFICATION")
    print("=" * 60)

    tests = [
        ("connect.sql", "Connection and schema verification"),
        ("basic_analysis.sql", "Basic statistical analysis"),
        ("insert.sql", "INSERT Duke Tech university"),
        ("query_japan.sql", "Count Japanese universities"),
        ("update_oxford.sql", "Update Oxford score"),
        ("delete_low_scores.sql", "Delete low-scoring universities"),
    ]

    results = {}
    for filename, description in tests:
        results[filename] = test_sql_file(filename, description)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    passed = sum(1 for r in results.values() if r)
    total = len(results)

    for filename, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {filename}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n✓✓✓ ALL SQL FILES ARE WORKING CORRECTLY! ✓✓✓")
        print("\nYou can now run:")
        print("  make run")
        print("  or")
        print("  python main.py")
    else:
        print("\n⚠ Some SQL files have issues. Please review the errors above.")

    print("=" * 60)


if __name__ == "__main__":
    main()
