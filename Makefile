.PHONY: clean format lint test coverage

default: clean

clean:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	rm -rf dist/ build/ .pytest_cache/

format:
	isort .
	black .

lint:
	isort --check-only --diff .
	black --check --diff .
	flake8 .

test:
	./runtests.py

coverage:
	coverage run ./runtests.py && coverage html
