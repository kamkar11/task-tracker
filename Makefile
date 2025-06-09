# Colors for better visibility
BLUE := \033[1;34m
GREEN := \033[1;32m
RED := \033[1;31m
YELLOW := \033[1;33m
NC := \033[0m # No Color

# Load environment variables from .env file if it exists
ifneq (,$(wildcard .env))
    include .env
    export
endif

.PHONY: help network build build-force task-tracker postgres up down logs clean test lint install env-file

# Default target when just running 'make'
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage:'
	@echo '  ${BLUE}make${NC} ${GREEN}<target>${NC}'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${BLUE}%-15s${NC} %s\n", $$1, $$2}' $(MAKEFILE_LIST)

#######################
# Environment Setup
#######################

env-file: ## Create .env file from template if it doesn't exist
	@if [ ! -f .env ]; then \
		if [ -f .env.example ]; then \
			echo "${BLUE}Creating .env file from template...${NC}"; \
			cp .env.example .env; \
			echo "${GREEN}.env file created successfully from template.${NC}"; \
		else \
			echo "${RED}Error: .env.example file not found!${NC}"; \
			exit 1; \
		fi \
	else \
		echo "${YELLOW}.env file already exists.${NC}"; \
	fi

#######################
# Docker Operations
#######################

network: ## Create shared Docker network
	@echo "${BLUE}Creating shared network...${NC}"
	@docker network create shared-network || true

build: ## Build base and migrator images
	@echo "${BLUE}Building base-python:3.12.5 if not exists...${NC}"
	@if [ "$$(docker images -q base-python:3.12.5 2> /dev/null)" = "" ]; then \
		docker build -f app/base_image/Dockerfile -t base-python:3.12.5 .; \
	else \
		echo "${GREEN}Image base-python:3.12.5 already exists${NC}"; \
	fi

# 	@echo "${BLUE}Building db-migrator image...${NC}"
# 	@if [ "$$(docker images -q db-migrator 2> /dev/null)" = "" ]; then \
# 		docker build -f app/microservices/db_migrator/Dockerfile -t db-migrator:latest .; \
# 	else \
# 		echo "${GREEN}Image db-migrator already exists${NC}"; \
# 	fi


build-force: ## Force rebuild base Python image
	@echo "${BLUE}Force rebuilding base Python image...${NC}"
	docker build --no-cache -f app/base_image/Dockerfile -t base-python:3.12.5 .

task-tracker: env-file ## Start task-tracker service
	@echo "${BLUE}Starting task-tracker service...${NC}"
	cd app/microservices/task_tracker/docker && docker compose up -d

db-migrator: env-file ## Start db-migrator and postgres services
	@echo "${BLUE}Starting db service...${NC}"
	docker compose -f app/microservices/postgres/docker/docker-compose.yaml \
	               -f app/microservices/db_migrator/docker/docker-compose.yaml up -d

up: network build db-migrator task-tracker ## Start all services
	@echo "${GREEN}All services are up!${NC}"

down: ## Stop all services
	@echo "${BLUE}Stopping all services...${NC}"
	cd app/microservices/task_tracker/docker && docker compose stop
	cd app/microservices/postgres/docker && docker compose stop
	@echo "${GREEN}All services stopped${NC}"

logs: ## View service logs (usage: make logs service=<service-name>)
	@if [ "$(service)" = "postgres" ]; then \
		echo "${BLUE}Showing PostgreSQL logs...${NC}" && \
		cd app/microservices/postgres/docker && docker compose logs -f; \
	elif [ "$(service)" = "task-tracker" ]; then \
		echo "${BLUE}Showing task-tracker logs...${NC}" && \
		cd app/microservices/task_tracker/docker && docker compose logs -f; \
	else \
		echo "${RED}Please specify a service: make logs service=<postgres|task-tracker>${NC}"; \
	fi

clean: down ## Clean up all containers, networks, and volumes
	@echo "${BLUE}Cleaning up Docker resources...${NC}"
	docker network rm shared-network || true
	docker system prune -f
	docker volume rm $$(docker volume ls -q) || true
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

postgres-shell: ## Open PostgreSQL shell
	@echo "${BLUE}Opening PostgreSQL shell...${NC}"
	cd app/microservices/postgres/docker && docker compose exec postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}


######################
# Alembic
#####################

alembic_migrate:
	docker compose -f app/microservices/postgres/docker/docker-compose.yaml \
	               -f app/microservices/db_migrator/docker/docker-compose.yaml \
	               run --rm db-migrator alembic revision --autogenerate -m "$(name)"

alembic_upgrade:
	docker compose -f app/microservices/postgres/docker/docker-compose.yaml \
	               -f app/microservices/db_migrator/docker/docker-compose.yaml \
	               run --rm db-migrator alembic upgrade head

alembic_downgrade:
	docker compose -f app/microservices/postgres/docker/docker-compose.yaml \
	               -f app/microservices/db_migrator/docker/docker-compose.yaml \
	               run --rm db-migrator alembic downgrade -1

alembic_history:
	docker compose -f app/microservices/postgres/docker/docker-compose.yaml \
	               -f app/microservices/db_migrator/docker/docker-compose.yaml \
	               run --rm db-migrator alembic history