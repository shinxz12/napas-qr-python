sources = qr_pay

.PHONY: install test format lint unittest coverage pre-commit build docs clean

install:
	uv sync

test: format lint unittest

format:
	uv run isort $(sources) tests
	uv run black $(sources) tests

lint:
	uv run flake8 $(sources) tests
	uv run mypy $(sources) tests

unittest:
	uv run pytest

coverage:
	uv run pytest --cov=$(sources) --cov-branch --cov-report=term-missing tests

pre-commit:
	uv run pre-commit run --all-files

build:
	uv build

docs:
	uv run --group doc mkdocs build

clean:
	rm -rf .mypy_cache .pytest_cache
	rm -rf *.egg-info
	rm -rf .tox dist site
	rm -rf coverage.xml .coverage
