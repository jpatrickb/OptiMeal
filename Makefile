.PHONY: help build up down restart logs shell-api shell-frontend shell-db migrate migrate-create test clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up

up-d: ## Start all services in detached mode
	docker-compose up -d

down: ## Stop all services
	docker-compose down

down-v: ## Stop all services and remove volumes
	docker-compose down -v

restart: ## Restart all services
	docker-compose restart

restart-api: ## Restart API service
	docker-compose restart api

restart-frontend: ## Restart frontend service
	docker-compose restart frontend

logs: ## View logs for all services
	docker-compose logs -f

logs-api: ## View API logs
	docker-compose logs -f api

logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

logs-db: ## View database logs
	docker-compose logs -f postgres

shell-api: ## Open shell in API container
	docker-compose exec api bash

shell-frontend: ## Open shell in frontend container
	docker-compose exec frontend sh

shell-db: ## Open PostgreSQL CLI
	docker-compose exec postgres psql -U optimeal_user -d optimeal_dev

migrate: ## Run database migrations
	docker-compose exec api alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create MESSAGE="description")
	docker-compose exec api alembic revision --autogenerate -m "$(MESSAGE)"

migrate-down: ## Rollback last migration
	docker-compose exec api alembic downgrade -1

test-api: ## Run backend tests
	docker-compose exec api pytest

test-frontend: ## Run frontend tests
	docker-compose exec frontend npm test

lint-api: ## Lint backend code
	docker-compose exec api ruff check .
	docker-compose exec api black --check src/

lint-frontend: ## Lint frontend code
	docker-compose exec frontend npm run lint

format-api: ## Format backend code
	docker-compose exec api black src/
	docker-compose exec api isort src/

install-api: ## Install backend dependencies
	docker-compose exec api pip install -r requirements.txt

install-frontend: ## Install frontend dependencies
	docker-compose exec frontend npm install

clean: ## Remove all containers, volumes, and images
	docker-compose down -v
	docker system prune -f

reset: clean build up-d ## Clean everything and start fresh

status: ## Show status of all containers
	docker-compose ps

health: ## Check health of all services
	@echo "Checking PostgreSQL..."
	@docker-compose exec postgres pg_isready -U optimeal_user || echo "PostgreSQL not ready"
	@echo "Checking API..."
	@curl -f http://localhost:8000/health || echo "API not healthy"
	@echo "Checking Frontend..."
	@curl -f http://localhost:5173 || echo "Frontend not ready"

backup-db: ## Backup database to backup.sql
	docker-compose exec postgres pg_dump -U optimeal_user optimeal_dev > backup.sql
	@echo "Database backed up to backup.sql"

restore-db: ## Restore database from backup.sql
	docker-compose exec -T postgres psql -U optimeal_user -d optimeal_dev < backup.sql
	@echo "Database restored from backup.sql"

init: ## Initialize project (first-time setup)
	@echo "Building containers..."
	docker-compose build
	@echo "Starting database..."
	docker-compose up -d postgres
	@echo "Waiting for database to be ready..."
	sleep 10
	@echo "Running migrations..."
	docker-compose exec api alembic upgrade head || echo "No migrations to run yet"
	@echo "Starting all services..."
	docker-compose up -d
	@echo "Done! Access the app at http://localhost:5173"
	@echo "API docs: http://localhost:8000/docs"
