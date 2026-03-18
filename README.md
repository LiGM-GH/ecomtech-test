# Migration tool

For this project, I'm using `yoyo-migrations`.

# How to run

The app has been tested for Ubuntu 24.04 (x86_64).

To build the project you will need [uv](https://docs.astral.sh/uv).

Then `.env` file must be filled as the pattern shows:

```.env
DB_CONN=postgresql://USERNAME:PASSWORD@DB_HOST:DB_PORT/DB_NAME
```

After the env file is created, `yoyo-migrations` workspace must be established:
```sh
uv run --locked yoyo init --database $DB_CONN migrations
```

The following command is used to run the app:
```sh
uv run --locked uvicorn main:app
```

# Docker

To run docker, multiple commands are required.
This is the script that starts the docker.

```sh
docker build . --file ./Dockerfile-uv.dockerfile --tag 'local-uv-image:latest'
docker-compose up
```
