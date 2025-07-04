# Makefile for cloudrun-init

.PHONY: help dev test lint clean docker-build docker-run deploy

# Default target
help:
	@echo "Available targets:"
	@echo "  dev          - Run Flask app locally with live reload"
	@echo "  test         - Run pytest"
	@echo "  lint         - Run flake8 linting"
	@echo "  clean        - Clean up Python cache files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container locally"
	@echo "  deploy       - Deploy to Cloud Run (requires gcloud setup)"

# Development
dev:
	@echo "Starting Flask development server..."
	@python -m flask --app app.main:app run --debug --host=0.0.0.0 --port=5000

# Testing
test:
	@echo "Running tests..."
	@pytest tests/ -v

# Linting
lint:
	@echo "Running flake8..."
	@flake8 app/ tests/ --max-line-length=100 --ignore=E501,W503

# Clean up
clean:
	@echo "Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +

# Docker commands
docker-build:
	@echo "Building Docker image..."
	@docker build -t cloudrun-init .

docker-run:
	@echo "Running Docker container..."
	@docker run -p 8080:8080 --env-file .env cloudrun-init

# Deployment (requires gcloud setup)
deploy:
	@echo "Deploying to Cloud Run..."
	@gcloud run deploy cloudrun-init \
		--image gcr.io/$(shell gcloud config get-value project)/cloudrun-init \
		--platform managed \
		--region us-central1 \
		--allow-unauthenticated \
		--port 8080

# Install dependencies
install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	@pip install -r requirements.txt
	@pip install pytest-cov black

# Format code
format:
	@echo "Formatting code with black..."
	@black app/ tests/

# Run with coverage
test-cov:
	@echo "Running tests with coverage..."
	@pytest tests/ --cov=app --cov-report=html --cov-report=term

# Check if .env file exists
check-env:
	@if [ ! -f .env ]; then \
		echo "Warning: .env file not found. Create one with your Firebase configuration."; \
		echo "Example .env file:"; \
		echo "FIREBASE_PROJECT_ID=your-project-id"; \
		echo "GOOGLE_CLOUD_PROJECT=your-project-id"; \
		echo "SECRET_KEY=your-secret-key"; \
	fi 