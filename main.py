"""
Main script to execute database operations for IDS706 Mini Assignment 6
"""

import sqlite3
import os


def execute_sql_file(cursor, filepath):
    """Execute SQL commands from a file"""
    with open(filepath, "r") as f:
        sql_script = f.read()
    # Split by semicolon and execute each statement
    statements = sql_script.split(";")
    results = []
    for statement in statements:
        statement = statement.strip()
        if statement and not statement.startswith("--"):
            try:
                cursor.execute(statement)
                # Fetch results if it's a SELECT statement
                if statement.upper().strip().startswith("SELECT"):
                    results.append(cursor.fetchall())
            except sqlite3.Error as e:
                print(f"Error executing statement: {e}")
                print(f"Statement: {statement[:100]}...")
    return results


def connect_to_database(db_path="university_database.db"):
    """Connect to the SQLite database"""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"✓ Successfully connected to {db_path}")
    return conn, cursor


def perform_basic_analysis(cursor):
    """Execute basic analysis queries"""
    print("\n" + "=" * 50)
    print("BASIC ANALYSIS")
    print("=" * 50)

    results = execute_sql_file(cursor, "basic_analysis.sql")
    print("✓ Basic analysis completed")
    return results


def perform_crud_operations(conn, cursor):
    """Execute all CRUD operations"""
    print("\n" + "=" * 50)
    print("CRUD OPERATIONS")
    print("=" * 50)

    # CREATE (INSERT)
    print("\n1. INSERT: Adding Duke Tech university for 2014...")
    execute_sql_file(cursor, "insert.sql")
    conn.commit()
    print("✓ Inserted Duke Tech university")

    # READ (QUERY)
    print("\n2. READ: Counting Japanese universities in top 200 (2013)...")
    results = execute_sql_file(cursor, "query_japan.sql")
    if results and results[0]:
        count = results[0][0][0]
        print(f"✓ Found {count} Japanese universities in top 200 for 2013")

    # UPDATE
    print("\n3. UPDATE: Updating Oxford score for 2014...")
    execute_sql_file(cursor, "update_oxford.sql")
    conn.commit()
    print("✓ Updated University of Oxford score (+1.2 points)")

    # DELETE
    print("\n4. DELETE: Removing universities with score < 45 in 2015...")
    results = execute_sql_file(cursor, "delete_low_scores.sql")
    conn.commit()
    print("✓ Deleted universities with score below 45 in 2015")


def main():
    """Main function to run all database operations"""
    try:
        # Connect to database
        conn, cursor = connect_to_database()

        # Verify connection
        print("\nVerifying connection...")
        execute_sql_file(cursor, "connect.sql")

        # Perform basic analysis
        perform_basic_analysis(cursor)

        # Perform CRUD operations
        perform_crud_operations(conn, cursor)

        # Close connection
        cursor.close()
        conn.close()
        print("\n" + "=" * 50)
        print("ALL OPERATIONS COMPLETED SUCCESSFULLY")
        print("=" * 50)

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()