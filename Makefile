.PHONY: help install test lint format run docker-build docker-run clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run code linting"
	@echo "  make format       - Format code with black"
	@echo "  make run          - Run the application"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make clean        - Clean up temporary files"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=app

lint:
	flake8 app tests
	pylint app

format:
	black app tests

run:
	python -m app.main

docker-build:
	docker build -t earthquake-detector:latest .

docker-run:
	docker run -d \
	  --name earthquake-detector \
	  -e MQTT_BROKER=localhost \
	  -p 8000:8000 \
	  -p 5000:5000 \
	  earthquake-detector:latest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf build/
	rm -rf dist/
