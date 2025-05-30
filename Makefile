PHONY: install shell clean rund logs help

lint:
	@echo "Formatting code..."
	pipenv run ruff check --fix .

fmt:
	@echo "Formatting code..."
	pipenv run ruff format .

install:
	@echo "Installing dev dependencies..."
	pipenv install --dev

shell: install
	@echo "Setting up the shell environment..."
	shell

clean:
	@echo "Cleaning up containers..."
	docker compose down --volumes --remove-orphans

rund: clean
	@echo "Spinning up containers..."
	docker compose up --build -d

logs:
	@echo "Displaying logs..."
	docker compose logs -f

help:
	@echo "Makefile for building and running the project"
	@echo "Available targets:"
	@echo "  install - Install project dependencies"
	@echo "  shell   - Open shell with virtual environment"
	@echo "  rund    - Start Docker containers"
	@echo "  logs    - Show logs from Docker containers"
	@echo "  clean   - Clean up Docker containers and volumes"
