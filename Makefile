.PHONY: setup run test clean

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && uvicorn app.main:app --reload

test:
	. venv/bin/activate && pytest tests/ -v

clean:
	rm -rf venv __pycache__ .pytest_cache *.db
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
