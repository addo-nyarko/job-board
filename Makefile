.PHONY: setup setup-dev run test lint format typecheck check clean

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

setup-dev:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements-dev.txt

run:
	. venv/bin/activate && uvicorn app.main:app --reload

test:
	. venv/bin/activate && pytest tests/ -v

lint:
	. venv/bin/activate && ruff check .

format:
	. venv/bin/activate && ruff format .

typecheck:
	. venv/bin/activate && mypy app/

check: lint typecheck test

clean:
	rm -rf venv __pycache__ .pytest_cache *.db
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
