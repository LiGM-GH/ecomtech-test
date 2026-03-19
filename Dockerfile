FROM local-uv-image:latest

WORKDIR /app

RUN mkdir migrations
RUN mkdir src
COPY ./migrations /app/migrations
COPY ./src/ /app/src
COPY ./main.py /app/

RUN uv sync --frozen
