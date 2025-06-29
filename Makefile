.PHONY: help install install-dev test test-cov lint format clean build publish

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install the package with development dependencies
	pip install -e .[dev]

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=dacp --cov-report=html --cov-report=term-missing

lint:  ## Run linting checks
	flake8 dacp/ tests/
	black --check --diff .
	mypy dacp/

format:  ## Format code with black
	black .

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build the package
	python -m build

publish:  ## Publish to PyPI (requires TWINE_USERNAME and TWINE_PASSWORD)
	twine upload dist/*

check-package:  ## Check the built package
	twine check dist/*

release: clean build check-package  ## Build and check package for release

all: install-dev lint test  ## Run all checks (install, lint, test) 