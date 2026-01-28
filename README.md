# Notification Service

Smart Notification Service — тестовый микросервис на FastAPI для приёма и имитации отправки уведомлений (email/telegram) с фоновыми задачами и повторными попытками.

## Возможности
- Создание уведомления с немедленным ответом (`pending`).
- Фоновая имитация отправки с задержкой и retry (до 3 попыток).
- История уведомлений по пользователю с фильтрацией по статусу.
- Асинхронный доступ к PostgreSQL (SQLAlchemy + asyncpg).
- Логирование запросов в STDOUT.

## Требования
- Python 3.11+
- Docker (для запуска через контейнеры)

## Переменные окружения
Сервис читает настройки из `.env`. Пример — [.env.example](.env.example).

Минимальные параметры:
- `APP_HOST`
- `APP_PORT`
- `DATABASE_URL`

Для Docker Compose также используются:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

## Запуск локально (без Docker)
1) Установить зависимости:

`uv pip install -e "[test]"`

2) Запустить PostgreSQL (например, через Docker):

`docker compose up -d db`

3) Запустить приложение:

`uv run uvicorn app.main:app --reload`

## Запуск через Docker Compose (рекомендуется)
1) Создай `.env` на основе [.env.example](.env.example).
2) Запуск:

`docker compose up --build`

Сервис будет доступен по адресу `http://localhost:${APP_PORT}`.

## Запуск только Docker (без compose)
1) Собрать образ:

`docker build -t notification-service .`

2) Запуск:

`docker run --env-file .env -p 8000:8000 notification-service`

## Тесты
`uv run pytest`

## API
- `POST /api/notifications`
- `GET /api/notifications/{user_id}?status=sent`

Swagger: `http://localhost:${APP_PORT}/docs`
