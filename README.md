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
- uv

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

## Запуск через Docker Compose (рекомендуется)
1) Создай `.env` на основе [.env.example](.env.example).
2) Запуск:

`docker compose up --build`

Сервис будет доступен по адресу `http://localhost:${APP_PORT}`.

## Запуск локально (без Docker)
1) Создать виртуальное окружение:

`uv venv`

2) Установить зависимости:

`uv pip install -e ".[test]"`

3) Запустить PostgreSQL (например, через Docker):

`docker compose up -d db`

4) Убедись, что в `.env` для локального запуска указан `localhost`:

`DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/notifications`

5) Запустить приложение:

`uv run uvicorn app.main:app --reload`

## Запуск с помощью Docker (без compose)
1) Собрать образ:

`docker build -t notification-service .`

2) Убедись, что БД запущена (рекомендуется через Docker Compose):

`docker compose up -d db`

3) Для запуска контейнера без compose укажи хост БД явно (контейнер не видит сервис `db`):

`DATABASE_URL=postgresql+asyncpg://postgres:postgres@host.docker.internal:5432/notifications`

4) Запуск:

`docker run --env-file .env -p 8000:8000 notification-service`

## Тесты
Требуется создать виртуальное окружение и установить зависимости:

`uv venv`
`uv pip install -e ".[test]"`

Запуск тестов:

`uv run pytest`

## Миграции
Миграции выполняются автоматически при старте приложения.
При необходимости можно выполнить вручную:

`uv run alembic upgrade head`

## API
## Статусы уведомлений
- `pending` — создано и ожидает отправки.
- `sent` — успешно отправлено.
- `failed` — не удалось отправить после 3 попыток.

### POST /api/notifications
Создаёт уведомление и возвращает его со статусом `pending`, не блокируя клиента.

Пример тела запроса:
`{"user_id": 123, "message": "Ваш код: 1111", "type": "telegram"}`

### GET /api/notifications/{user_id}?status=sent
Возвращает список уведомлений пользователя. Параметр `status` опционален и фильтрует по статусу.

## Swagger: 
`http://localhost:${APP_PORT}/docs` - документация.
