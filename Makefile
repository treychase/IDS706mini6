install:
	pip install --upgrade pip && pip install -r requirements.txt

format:
	black *.py

lint:
	ruff check *.py
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py

test:
	python -m pytest -vv --cov=. --cov-report=term-missing --cov-report=html test_main.py

test-simple:
	python -m pytest -vv test_main.py

run:
	python main.py

# SQL commands using Python (works without sqlite3 CLI)
connect:
	python run_sql.py connect.sql

analysis:
	python run_sql.py basic_analysis.sql

analysis-detailed:
	python show_analysis.py

insert:
	python run_sql.py insert.sql

query:
	python run_sql.py query_japan.sql

update:
	python run_sql.py update_oxford.sql

delete:
	python run_sql.py delete_low_scores.sql

# Alternative: Install sqlite3 CLI if needed
install-sqlite:
	sudo apt-get update && sudo apt-get install -y sqlite3

all: install format lint test run

clean:
	rm -rf __pycache__ .pytest_cache .coverage test_university_database.db htmlcov

.PHONY: install format lint test test-simple run connect analysis analysis-detailed insert query update delete install-sqlite all clean