install:
	pip install --upgrade pip && pip install -r requirements.txt

format:
	black *.py

lint:
	ruff check *.py
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py

test:
	python -m pytest -vv --cov=main --cov-report=term-missing test_main.py

run:
	python main.py

connect:
	sqlite3 university_database.db < connect.sql

analysis:
	sqlite3 university_database.db < basic_analysis.sql

insert:
	sqlite3 university_database.db < insert.sql

query:
	sqlite3 university_database.db < query_japan.sql

update:
	sqlite3 university_database.db < update_oxford.sql

delete:
	sqlite3 university_database.db < delete_low_scores.sql

all: install format lint test run

clean:
	rm -rf __pycache__ .pytest_cache .coverage test_university_database.db

.PHONY: install format lint test run connect analysis insert query update delete all clean