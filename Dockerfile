FROM local-uv-image:latest

WORKDIR /app

RUN mkdir migrations
RUN mkdir models
COPY ./migrations /app/migrations
COPY ./models/mark.py /app/models
COPY ./main.py /app/

RUN uv sync --frozen
