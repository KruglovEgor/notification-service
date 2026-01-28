FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml /app/
COPY uv.lock /app/
COPY README.md /app/
COPY app /app/app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000

EXPOSE ${APP_PORT}

CMD ["python", "-m", "app.run"]
