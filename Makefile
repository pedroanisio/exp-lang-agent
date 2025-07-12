# AI Linguistics Agent - Makefile
# 
# This Makefile provides common development, testing, and deployment commands
# for the AI Linguistics Agent project following TDD methodology and best practices.
#
# Rule Compliance: rules-101 v1.2+ (TDD), rules-103 v1.2+ (Implementation), rules-106 v1.0+ (Linting)

.PHONY: help install install-dev test test-unit test-integration test-coverage clean clean-all lint format type-check security-check docker-build docker-up docker-down docker-test deploy-dev deploy-prod backup restore docs serve-docs git-hooks pre-commit tdd-red tdd-green tdd-refactor

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3.11
PIP := pip3
PYTEST := pytest
DOCKER_COMPOSE := docker-compose
PROJECT_NAME := ai-linguistics-agent
SRC_DIR := src
TEST_DIR := tests
DOCS_DIR := docs
VENV_DIR := .venv

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
WHITE := \033[0;37m
RESET := \033[0m

##@ Help

help: ## Display this help message
	@echo "$(CYAN)AI Linguistics Agent - Development Makefile$(RESET)"
	@echo ""
	@echo "$(YELLOW)Usage:$(RESET)"
	@echo "  make <target>"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\nAvailable targets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(CYAN)%-20s$(RESET) %s\n", $$1, $$2 } /^##@/ { printf "\n$(PURPLE)%s$(RESET)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Environment Setup

install: ## Install production dependencies
	@echo "$(BLUE)Installing production dependencies...$(RESET)"
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(RESET)"
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .
	@echo "$(GREEN)Development environment ready!$(RESET)"

venv: ## Create virtual environment
	@echo "$(BLUE)Creating virtual environment...$(RESET)"
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "$(GREEN)Virtual environment created. Activate with: source $(VENV_DIR)/bin/activate$(RESET)"

setup: venv install-dev git-hooks ## Complete development environment setup
	@echo "$(GREEN)Development environment setup complete!$(RESET)"

##@ Testing (TDD Workflow)

test: ## Run all tests
	@echo "$(BLUE)Running all tests...$(RESET)"
	$(PYTEST) $(TEST_DIR) -v --tb=short

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(RESET)"
	$(PYTEST) $(TEST_DIR)/unit -v --tb=short

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(RESET)"
	$(PYTEST) $(TEST_DIR)/integration -v --tb=short

test-coverage: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(RESET)"
	$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term --cov-report=xml --cov-fail-under=80

test-watch: ## Run tests in watch mode (requires pytest-watch)
	@echo "$(BLUE)Running tests in watch mode...$(RESET)"
	ptw $(TEST_DIR) $(SRC_DIR) -- -v

test-fast: ## Run tests with minimal output (for TDD cycles)
	@echo "$(BLUE)Running fast tests...$(RESET)"
	$(PYTEST) $(TEST_DIR) -q --tb=no

##@ TDD Workflow Support

tdd-red: ## TDD RED phase - run tests expecting failures
	@echo "$(RED)TDD RED PHASE: Running tests (expecting failures)...$(RESET)"
	@$(PYTEST) $(TEST_DIR) -v --tb=short || echo "$(RED)✓ Tests failing as expected in RED phase$(RESET)"

tdd-green: ## TDD GREEN phase - run tests expecting success
	@echo "$(GREEN)TDD GREEN PHASE: Running tests (expecting success)...$(RESET)"
	$(PYTEST) $(TEST_DIR) -v --tb=short
	@echo "$(GREEN)✓ All tests passing - GREEN phase complete$(RESET)"

tdd-refactor: test-coverage lint ## TDD REFACTOR phase - run full quality checks
	@echo "$(PURPLE)TDD REFACTOR PHASE: Running quality checks...$(RESET)"
	@echo "$(GREEN)✓ REFACTOR phase complete - code quality verified$(RESET)"

tdd-cycle: tdd-red tdd-green tdd-refactor ## Complete TDD cycle (RED-GREEN-REFACTOR)
	@echo "$(CYAN)✓ Complete TDD cycle finished successfully$(RESET)"

##@ Code Quality

lint: ## Run all linting checks
	@echo "$(BLUE)Running linting checks...$(RESET)"
	ruff check $(SRC_DIR) $(TEST_DIR)
	black --check $(SRC_DIR) $(TEST_DIR)
	isort --check-only $(SRC_DIR) $(TEST_DIR)

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(RESET)"
	black $(SRC_DIR) $(TEST_DIR)
	isort $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)Code formatting complete!$(RESET)"

type-check: ## Run type checking with mypy
	@echo "$(BLUE)Running type checks...$(RESET)"
	mypy $(SRC_DIR) --config-file=.linting/configs/mypy.ini

security-check: ## Run security checks with bandit
	@echo "$(BLUE)Running security checks...$(RESET)"
	bandit -r $(SRC_DIR) -f json -o security-report.json
	bandit -r $(SRC_DIR)

quality: lint type-check security-check ## Run all quality checks
	@echo "$(GREEN)All quality checks passed!$(RESET)"

##@ Database Operations

db-init: ## Initialize database with tables
	@echo "$(BLUE)Initializing database...$(RESET)"
	$(PYTHON) -c "from src.linguistics_agent.database import DatabaseManager; import asyncio; asyncio.run(DatabaseManager('sqlite:///linguistics.db').initialize())"

db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(RESET)"
	alembic upgrade head

db-reset: ## Reset database (WARNING: destroys all data)
	@echo "$(RED)Resetting database (this will destroy all data)...$(RESET)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -f linguistics.db linguistics-test.db; \
		$(MAKE) db-init; \
		echo "$(GREEN)Database reset complete!$(RESET)"; \
	else \
		echo "$(YELLOW)Database reset cancelled.$(RESET)"; \
	fi

##@ Docker Operations

docker-build: ## Build Docker containers
	@echo "$(BLUE)Building Docker containers...$(RESET)"
	$(DOCKER_COMPOSE) build

docker-up: ## Start Docker containers
	@echo "$(BLUE)Starting Docker containers...$(RESET)"
	$(DOCKER_COMPOSE) up -d

docker-down: ## Stop Docker containers
	@echo "$(BLUE)Stopping Docker containers...$(RESET)"
	$(DOCKER_COMPOSE) down

docker-logs: ## View Docker container logs
	@echo "$(BLUE)Viewing Docker logs...$(RESET)"
	$(DOCKER_COMPOSE) logs -f

docker-test: ## Run tests in Docker environment
	@echo "$(BLUE)Running tests in Docker...$(RESET)"
	$(DOCKER_COMPOSE) -f docker-compose.test.yml up --build --abort-on-container-exit

docker-shell: ## Open shell in main container
	@echo "$(BLUE)Opening shell in main container...$(RESET)"
	$(DOCKER_COMPOSE) exec app /bin/bash

docker-clean: ## Clean Docker containers and images
	@echo "$(BLUE)Cleaning Docker containers and images...$(RESET)"
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	docker system prune -f

##@ Development Server

serve: ## Start development server
	@echo "$(BLUE)Starting development server...$(RESET)"
	uvicorn linguistics_agent.api.main:app --host 0.0.0.0 --port 8000 --reload --app-dir $(SRC_DIR)

serve-prod: ## Start production server
	@echo "$(BLUE)Starting production server...$(RESET)"
	uvicorn linguistics_agent.api.main:app --host 0.0.0.0 --port 8000 --workers 4 --app-dir $(SRC_DIR)

##@ Documentation

docs: ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(RESET)"
	@mkdir -p $(DOCS_DIR)
	@echo "# AI Linguistics Agent Documentation" > $(DOCS_DIR)/README.md
	@echo "Documentation generated in $(DOCS_DIR)/"

serve-docs: docs ## Serve documentation locally
	@echo "$(BLUE)Serving documentation...$(RESET)"
	@cd $(DOCS_DIR) && $(PYTHON) -m http.server 8080

api-docs: ## Generate API documentation
	@echo "$(BLUE)API documentation available at: http://localhost:8000/docs$(RESET)"
	@echo "$(BLUE)ReDoc documentation available at: http://localhost:8000/redoc$(RESET)"

##@ Cleaning

clean: ## Clean temporary files and caches
	@echo "$(BLUE)Cleaning temporary files...$(RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf dist/
	rm -rf build/
	@echo "$(GREEN)Cleanup complete!$(RESET)"

clean-all: clean docker-clean ## Clean everything including Docker
	@echo "$(BLUE)Deep cleaning...$(RESET)"
	rm -rf $(VENV_DIR)
	rm -rf node_modules/
	rm -f linguistics.db linguistics-test.db
	@echo "$(GREEN)Deep cleanup complete!$(RESET)"

##@ Git and Version Control

git-hooks: ## Install git hooks for pre-commit
	@echo "$(BLUE)Installing git hooks...$(RESET)"
	pre-commit install
	@echo "$(GREEN)Git hooks installed!$(RESET)"

pre-commit: ## Run pre-commit hooks manually
	@echo "$(BLUE)Running pre-commit hooks...$(RESET)"
	pre-commit run --all-files

commit-check: quality test ## Run all checks before committing
	@echo "$(GREEN)All checks passed - ready to commit!$(RESET)"

##@ Deployment

deploy-dev: ## Deploy to development environment
	@echo "$(BLUE)Deploying to development environment...$(RESET)"
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml up --build -d
	@echo "$(GREEN)Development deployment complete!$(RESET)"

deploy-prod: ## Deploy to production environment
	@echo "$(BLUE)Deploying to production environment...$(RESET)"
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml up --build -d
	@echo "$(GREEN)Production deployment complete!$(RESET)"

##@ Backup and Restore

backup: ## Backup database and important files
	@echo "$(BLUE)Creating backup...$(RESET)"
	@mkdir -p backups
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	cp linguistics.db backups/linguistics_$$timestamp.db 2>/dev/null || true; \
	tar -czf backups/project_$$timestamp.tar.gz $(SRC_DIR) $(TEST_DIR) requirements*.txt pyproject.toml .braains/ 2>/dev/null || true
	@echo "$(GREEN)Backup created in backups/ directory$(RESET)"

restore: ## Restore from backup (interactive)
	@echo "$(BLUE)Available backups:$(RESET)"
	@ls -la backups/ 2>/dev/null || echo "No backups found"
	@echo "$(YELLOW)Use 'cp backups/linguistics_TIMESTAMP.db linguistics.db' to restore database$(RESET)"

##@ Monitoring and Health

health: ## Check system health
	@echo "$(BLUE)Checking system health...$(RESET)"
	@echo "$(CYAN)Python version:$(RESET) $$($(PYTHON) --version)"
	@echo "$(CYAN)Pip version:$(RESET) $$($(PIP) --version)"
	@echo "$(CYAN)Docker version:$(RESET) $$(docker --version 2>/dev/null || echo 'Not installed')"
	@echo "$(CYAN)Database status:$(RESET) $$(test -f linguistics.db && echo 'Present' || echo 'Not found')"
	@echo "$(CYAN)Virtual environment:$(RESET) $$(test -d $(VENV_DIR) && echo 'Present' || echo 'Not found')"

status: ## Show project status
	@echo "$(CYAN)AI Linguistics Agent - Project Status$(RESET)"
	@echo "$(BLUE)Git branch:$(RESET) $$(git branch --show-current 2>/dev/null || echo 'Not a git repository')"
	@echo "$(BLUE)Git status:$(RESET)"
	@git status --porcelain 2>/dev/null || echo "Not a git repository"
	@echo "$(BLUE)Last commit:$(RESET) $$(git log -1 --oneline 2>/dev/null || echo 'No commits')"
	@echo "$(BLUE)Docker containers:$(RESET)"
	@$(DOCKER_COMPOSE) ps 2>/dev/null || echo "Docker not running or no containers"

##@ Performance and Profiling

profile: ## Run performance profiling
	@echo "$(BLUE)Running performance profiling...$(RESET)"
	$(PYTHON) -m cProfile -o profile.stats -m pytest $(TEST_DIR)/unit -q
	@echo "$(GREEN)Profile saved to profile.stats$(RESET)"

benchmark: ## Run benchmark tests
	@echo "$(BLUE)Running benchmark tests...$(RESET)"
	$(PYTEST) $(TEST_DIR) -m benchmark -v

##@ Utilities

requirements: ## Generate requirements.txt from pyproject.toml
	@echo "$(BLUE)Generating requirements.txt...$(RESET)"
	pip-compile pyproject.toml --output-file requirements.txt
	pip-compile pyproject.toml --extra dev --output-file requirements-dev.txt
	@echo "$(GREEN)Requirements files updated!$(RESET)"

check-deps: ## Check for dependency updates
	@echo "$(BLUE)Checking for dependency updates...$(RESET)"
	pip list --outdated

update-deps: ## Update dependencies (use with caution)
	@echo "$(YELLOW)Updating dependencies...$(RESET)"
	pip install --upgrade pip
	pip install --upgrade -r requirements-dev.txt

##@ Information

info: ## Show project information
	@echo "$(CYAN)AI Linguistics Agent - Project Information$(RESET)"
	@echo "$(BLUE)Project:$(RESET) AI Linguistics Agent"
	@echo "$(BLUE)Version:$(RESET) $$(grep version pyproject.toml | cut -d'"' -f2 2>/dev/null || echo 'Unknown')"
	@echo "$(BLUE)Python:$(RESET) $(PYTHON)"
	@echo "$(BLUE)Source:$(RESET) $(SRC_DIR)/"
	@echo "$(BLUE)Tests:$(RESET) $(TEST_DIR)/"
	@echo "$(BLUE)Documentation:$(RESET) http://localhost:8000/docs (when server running)"
	@echo "$(BLUE)Repository:$(RESET) $$(git remote get-url origin 2>/dev/null || echo 'Local repository')"

version: ## Show version information
	@echo "$(CYAN)Version Information:$(RESET)"
	@echo "$(BLUE)Project:$(RESET) $$(grep version pyproject.toml | cut -d'"' -f2 2>/dev/null || echo 'Unknown')"
	@echo "$(BLUE)Python:$(RESET) $$($(PYTHON) --version)"
	@echo "$(BLUE)FastAPI:$(RESET) $$($(PYTHON) -c 'import fastapi; print(fastapi.__version__)' 2>/dev/null || echo 'Not installed')"
	@echo "$(BLUE)Pytest:$(RESET) $$($(PYTEST) --version | head -1 2>/dev/null || echo 'Not installed')"

##@ Quick Commands

quick-test: test-fast ## Quick test run for TDD cycles
quick-check: lint type-check ## Quick quality check
quick-start: install-dev serve ## Quick start for development
quick-deploy: docker-build docker-up ## Quick Docker deployment

# Special targets for common workflows
dev: install-dev git-hooks ## Setup development environment
ci: quality test-coverage ## Run CI checks
cd: deploy-prod ## Continuous deployment

