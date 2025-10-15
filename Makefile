.PHONY: help install dev test lint type sec format clean docker run

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -e .

dev:  ## Install development dependencies
	pip install -e ".[dev]"

run:  ## Run the development server
	uvicorn app.main:app --reload --port 8000

test:  ## Run tests with coverage
	pytest -v --cov=app --cov-report=term-missing --cov-report=html

test-fast:  ## Run tests without coverage
	pytest -v

lint:  ## Run ruff linter
	ruff check app/ tests/

lint-fix:  ## Run ruff linter with auto-fix
	ruff check --fix app/ tests/

format:  ## Format code with ruff
	ruff format app/ tests/

type:  ## Run mypy type checker
	mypy app/

sec:  ## Run bandit security scanner
	bandit -r app/ -c pyproject.toml

quality: lint type sec  ## Run all quality checks

ci: quality test  ## Run CI checks (quality + tests)

clean:  ## Clean up cache and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache
	rm -rf build dist *.egg-info

docker:  ## Build Docker image
	docker build -t apibridge-pro:latest .

docker-run:  ## Run Docker container
	docker run -p 8000:8000 \
		-e OPENWEATHER_KEY=${OPENWEATHER_KEY} \
		-e WEATHERAPI_KEY=${WEATHERAPI_KEY} \
		-e GITHUB_TOKEN=${GITHUB_TOKEN} \
		apibridge-pro:latest

docker-compose:  ## Run with docker-compose
	docker-compose up --build

benchmark:  ## Run simple benchmark
	python tests/benchmark.py

.DEFAULT_GOAL := help


