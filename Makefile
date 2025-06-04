.PHONY: network build task-tracker up

network:
	docker network create shared-network || true

build:
	docker build -f app/base_image/Dockerfile -t base-python:3.12.5 .

task-tracker:
	cd app/microservices/task_tracker/docker && docker compose up --build -d

up: task-tracker