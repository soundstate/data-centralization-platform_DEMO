# Data Centralization Platform Makefile

.PHONY: help setup build test lint clean docker-up docker-down deploy

# Default target
help:
	@echo "Available targets:"
	@echo "  setup      - Install dependencies and setup development environment"
	@echo "  build      - Build all services and UI components"
	@echo "  test       - Run all tests"
	@echo "  lint       - Run linting across all projects"
	@echo "  clean      - Clean build artifacts"
	@echo "  docker-up  - Start all services using Docker Compose"
	@echo "  docker-down- Stop all Docker services"
	@echo "  deploy     - Deploy to staging environment"

# Setup development environment
setup:
	@echo "Setting up development environment..."
	npm install
	@echo "Creating environment files from templates..."
	cp infrastructure/environment/.env.development.template infrastructure/environment/.env.development || true
	@echo "Setup complete!"

# Build all components
build:
	@echo "Building all components..."
	npm run build
	@echo "Build complete!"

# Run tests
test:
	@echo "Running tests..."
	npm run test
	@echo "Tests complete!"

# Lint code
lint:
	@echo "Running linters..."
	npm run lint
	@echo "Linting complete!"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/* dist/* node_modules/.cache
	find . -name "node_modules" -type d -prune -exec rm -rf {} +
	@echo "Clean complete!"

# Docker operations
docker-up:
	@echo "Starting Docker services..."
	docker-compose -f infrastructure/docker/docker-compose.yml up -d
	@echo "Docker services started!"

docker-down:
	@echo "Stopping Docker services..."
	docker-compose -f infrastructure/docker/docker-compose.yml down
	@echo "Docker services stopped!"

# Deploy to staging
deploy:
	@echo "Deploying to staging..."
	cd infrastructure/terraform && terraform apply -auto-approve
	@echo "Deployment complete!"
