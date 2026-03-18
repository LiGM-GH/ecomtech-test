FROM local-uv-image:latest

WORKDIR /app

RUN mkdir migrations
RUN mkdir models
RUN mkdir src
COPY ./migrations /app/migrations
COPY ./models/ /app/models
COPY ./src/ /app/src
COPY ./main.py /app/

RUN uv sync --frozen
