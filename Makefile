.PHONY: help install dev-install lint format test test-coverage clean docker-build docker-run docker-stop

CODE := src
PYTHON := python
POETRY := python -m poetry
DOCKER_IMAGE := ai-code-reviewer:latest
DOCKER_CONTAINER := ai-code-reviewer-app
ENTRY_APP := $(POETRY) run python -m src

BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m

help: ## Показать это сообщение с помощью
	@echo "$(BLUE)AI Code Reviewer - Makefile:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Установить зависимости для продакшена
	$(POETRY) install --no-dev

dev-install: ## Установить все зависимости для разработки
	$(POETRY) install

lint: ## Проверить код линтерами
	$(POETRY) run flake8 $(CODE) --count --select=E9,F63,F7,F82 --show-source --statistics
	$(POETRY) run flake8 $(CODE) --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
	$(POETRY) run black --check --diff $(CODE)
	$(POETRY) run isort --check-only --diff $(CODE)
	@echo ""

format: ## Отформатировать код
	$(POETRY) run black $(CODE)
	$(POETRY) run isort $(CODE)

test: ## Запустить тесты
	$(POETRY) run pytest -v

test-coverage: ## Запустить тесты с покрытием
	$(POETRY) run pytest --cov=$(CODE) --cov-report=html --cov-report=term-missing

run-local: ## Запустить приложение локально
	$(ENTRY_APP) run $(ENTRY_APP)

docker-build: ## Собрать Docker образ
	docker build --no-cache -t $(DOCKER_IMAGE) .

docker-run: ## Запустить Docker контейнер
	docker run -d --name $(DOCKER_CONTAINER) $(DOCKER_IMAGE)

docker-stop: ## Остановить Docker контейнер
	docker stop $(DOCKER_CONTAINER) || true
	docker rm $(DOCKER_CONTAINER) || true

docker-compose-up: ## Запустить через docker-compose
	docker-compose up -d

docker-compose-down: ## Остановить docker-compose
	docker-compose down

docker-logs: ## Показать логи контейнера
	docker logs -f $(DOCKER_CONTAINER)

clean: ## Очистить временные файлы
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf dist/
	rm -rf build/

security: ## Проверить безопасность зависимостей
	$(POETRY) run safety check

pre-commit: lint test ## Запустить pre-commit проверки

update: ## Обновить зависимости
	$(POETRY) update

setup-hooks: ## Установить pre-commit хуки
	$(POETRY) run pre-commit install

requirements: ## Экспортировать requirements.txt
	$(POETRY) export -f requirements.txt --output requirements.txt --without-hashes

type-check: ## Проверить типы с mypy
	$(POETRY) run mypy $(CODE)

check-all: format lint type-check test ## Запустить все проверки

shell: ## Активировать poetry shell
	$(POETRY) shell