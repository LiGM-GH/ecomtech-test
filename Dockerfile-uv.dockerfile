FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY ./pyproject.toml /app/
COPY ./uv.lock /app/

RUN uv sync --frozen
