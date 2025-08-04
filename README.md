# 🤖 AI Code Reviewer

Интеллектуальный агент для автоматического ревью Python кода с использованием AI.

## 📋 Описание

AI Code Reviewer — это микросервис, который предоставляет API для анализа Python кода с помощью искусственного интеллекта. Сервис построен с использованием чистой архитектуры и предлагает различные виды анализа кода: от быстрых проверок до детального ревью.

## ✨ Возможности

- **Полное ревью кода** — детальный анализ с рекомендациями по улучшению
- **Быстрая проверка** — мгновенное выявление критических проблем
- **Объяснение проблем** — детальное разъяснение найденных issues
- **Сравнение версий** — анализ различий между версиями кода
- **REST API** с документацией Swagger
- **Docker поддержка** для легкого развертывания

## 🏗 Архитектура

Проект использует принципы чистой архитектуры:

```
src/
├── presentation/    # Слой представления (API endpoints)
├── application/     # Слой приложения (use cases)
├── domain/         # Доменный слой (бизнес-логика)
├── core/           # Ядро (конфигурация, интерфейсы)
├── infra/          # Инфраструктурный слой
└── tests/          # Тесты
```

## 🚀 Быстрый старт

### Требования

- Python 3.11+
- Poetry
- Docker (опционально)

### Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd code-review-agent
```

2. Установите зависимости:
```bash
make dev-install
```

3. Создайте файл `.env` с настройками:
```bash
LLM_OPENAI_API_KEY=your-openai-api-key
LLM_OPENAI_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2000
LLM_VERBOSE=true
```

4. Запустите сервис:
```bash
make run
```

Сервис будет доступен по адресу: http://localhost:8000

## 🐳 Docker

### Запуск с Docker Compose

```bash
docker-compose up --build
```

### Ручная сборка

```bash
make docker-build
make docker-run
```

## 📡 API Endpoints

### Основные endpoints:

- `GET /` — информация о сервисе
- `GET /api/v1/code-review/health` — проверка здоровья сервиса

### Code Review endpoints:

- `POST /api/v1/code-review/review` — полное ревью кода
- `POST /api/v1/code-review/quick-check` — быстрая проверка
- `POST /api/v1/code-review/explain` — объяснение проблемы
- `POST /api/v1/code-review/compare` — сравнение версий

### Примеры запросов:

#### Полное ревью кода
```bash
curl -X POST "http://localhost:8000/api/v1/code-review/review" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def calculate(x, y):\n    return x + y",
    "context": "Функция для сложения двух чисел",
    "format": "detailed"
  }'
```

#### Быстрая проверка
```bash
curl -X POST "http://localhost:8000/api/v1/code-review/quick-check" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def divide(a, b):\n    return a / b"
  }'
```

## 🛠 Разработка

### Доступные команды

```bash
make help              # Показать все доступные команды
make dev-install       # Установить зависимости для разработки
make lint              # Проверить код линтерами
make format            # Отформатировать код
make test              # Запустить тесты
make test-coverage     # Запустить тесты с покрытием
make run               # Запустить приложение
make clean             # Очистить временные файлы
```

### Инструменты качества кода

- **Ruff** — быстрый линтер и форматтер
- **MyPy** — статическая типизация
- **Black** — форматтер кода
- **Pytest** — тестирование
- **isort** — сортировка импортов

## 🔧 Конфигурация

Сервис настраивается через переменные окружения с префиксом `LLM_`:

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `LLM_OPENAI_API_KEY` | API ключ OpenAI | обязательно |
| `LLM_OPENAI_MODEL` | Модель OpenAI | `gpt-3.5-turbo` |
| `LLM_TEMPERATURE` | Температура модели | `0.1` |
| `LLM_MAX_TOKENS` | Максимум токенов | `2000` |
| `LLM_VERBOSE` | Подробный вывод | `true` |

## 📊 Мониторинг

- **Health check**: `GET /api/v1/code-review/health`
- **Service info**: `GET /`
- **API docs**: `GET /docs` (Swagger UI)
- **OpenAPI schema**: `GET /openapi.json`

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/new-feature`)
3. Внесите изменения и добавьте тесты
4. Запустите проверки качества кода (`make lint test`)
5. Закоммитьте изменения (`git commit -am 'Add new feature'`)
6. Отправьте в ветку (`git push origin feature/new-feature`)
7. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией [MIT](LICENSE).

## 🔗 Технологии

- **FastAPI** — веб-фреймворк
- **LangChain** — фреймворк для работы с LLM
- **OpenAI** — языковые модели
- **Pydantic** — валидация данных
- **Poetry** — управление зависимостями
- **Docker** — контейнеризация
- **Dependency Injector** — внедрение зависимостей