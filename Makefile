# Colors for better visibility
BLUE := \033[1;34m
GREEN := \033[1;32m
RED := \033[1;31m
YELLOW := \033[1;33m
NC := \033[0m # No Color

.PHONY: help network build build-force task-tracker task-tracker-build up up-build down logs clean test lint install

# Default target when just running 'make'
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage:'
	@echo '  ${BLUE}make${NC} ${GREEN}<target>${NC}'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${BLUE}%-15s${NC} %s\n", $$1, $$2}' $(MAKEFILE_LIST)

#######################
# Docker Operations
#######################

network: ## Create shared Docker network
	@echo "${BLUE}Creating shared network...${NC}"
	@docker network create shared-network || true

build: ## Build base Python image (only if not exists)
	@echo "${BLUE}Building base Python image if not exists...${NC}"
	@if [ "$$(docker images -q base-python:3.12.5 2> /dev/null)" = "" ]; then \
		docker build -f app/base_image/Dockerfile -t base-python:3.12.5 .; \
	else \
		echo "${GREEN}Image base-python:3.12.5 already exists${NC}"; \
	fi

build-force: ## Force rebuild base Python image
	@echo "${BLUE}Force rebuilding base Python image...${NC}"
	docker build --no-cache -f app/base_image/Dockerfile -t base-python:3.12.5 .

task-tracker: ## Start task-tracker service (without rebuild)
	@echo "${BLUE}Starting task-tracker service...${NC}"
	cd app/microservices/task_tracker/docker && docker compose up -d

task-tracker-build: ## Start task-tracker service with rebuild
	@echo "${BLUE}Starting task-tracker service with rebuild...${NC}"
	cd app/microservices/task_tracker/docker && docker compose up --build -d

up: network build task-tracker ## Start all services (without rebuild)
	@echo "${GREEN}All services are up!${NC}"

up-build: network build-force task-tracker-build ## Start all services with rebuild
	@echo "${GREEN}All services are up with fresh builds!${NC}"

down: ## Stop all services
	@echo "${BLUE}Stopping all services...${NC}"
	cd app/microservices/task_tracker/docker && docker compose down
	@echo "${GREEN}All services stopped${NC}"

logs: ## View task-tracker logs
	@echo "${BLUE}Showing task-tracker logs...${NC}"
	cd app/microservices/task_tracker/docker && docker compose logs -f

clean: down ## Clean up all containers and networks
	@echo "${BLUE}Cleaning up Docker resources...${NC}"
	docker network rm shared-network || true
	docker system prune -f
	@echo "${GREEN}Cleanup complete${NC}"

#######################
# Development
#######################

install: ## Install Python dependencies
	@echo "${BLUE}Installing Python dependencies...${NC}"
	pip install -r app/base_image/requirements.txt
	@echo "${GREEN}Dependencies installed${NC}"

lint: ## Run linters
	@echo "${BLUE}Running linters...${NC}"
	pip install black isort flake8
	black .
	isort .
	flake8 .
	@echo "${GREEN}Linting complete${NC}"

test: ## Run tests
	@echo "${BLUE}Running tests...${NC}"
	python -m pytest tests/ -v
	@echo "${GREEN}Tests complete${NC}"

#######################
# Utility
#######################

ps: ## Show running containers
	@echo "${BLUE}Running containers:${NC}"
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

restart: down up ## Restart all services (without rebuild)
	@echo "${GREEN}Services restarted${NC}"

restart-build: down up-build ## Restart all services with rebuild
	@echo "${GREEN}Services restarted with fresh builds${NC}"