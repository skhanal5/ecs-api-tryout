PHONY: install shell rund help

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
