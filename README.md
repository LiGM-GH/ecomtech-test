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

# Project structure

Overall project structure is as follows:

```
├── docker-compose.yml
├── Dockerfile
├── Dockerfile-uv.dockerfile
├── justfile
├── main.py
├── migrations
│   └── ...
├── pyproject.toml
├── src
│   ├── models
│   │   └── mark.py
│   ├── queries
│   │   └── queries.py
│   └── requests
│       ├── students.py
│       └── upload.py
└── uv.lock
```

## Python structure

Project is divided into three branches, `models`, `queries` and `requests`.

The former branch, `models`, is only used for validation.
Classes in it dictate the shapes of the values to be put in the DB and to be acquired from the user.
You can further familiarize yourself with the branch in its directory, `./src/models`.

The next branch, `queries`, manages the database interactions,
such as inserting values into the database and getting them out.
Each method in this branch more or less has its own return type specialized for its own needs.
This branch also has its own directory, `./src/queries`.

The last branch, `requests`, manages API handles.
It also has its own directory, `./src/requests`.
The files inside are divided hierarchically based on the API handle path.

## Docker structure

As it can be seen on the project tree (overall project structure), there are two dockerfiles and one docker-compose.yml.
Here, the `./Dockerfile` is used as the "main dockerfile",
while the other one, `./Dockerfile-uv.dockerfile`, is used as a cache to store Python and its dependencies.
That is for a couple of reasons.

The main reason is that recompiling the dependencies image and re-downloading Python and all the dependencies is quite suboptimal in terms of Internet usage and also very slow, which means slower feedback cycle and slower debug.
Also, Python dependencies don't change often, and when they do, it's easily detectable.

Using a prebuilt image most of the time and rebuilding it once the dependencies list changes is more reasonable.

For the best development experience, it is recommended to use [just, the command runner](https://just.systems/man/en) to build the Docker image.

The `start` recipe:
- first checks for the changes in `uv.lock` and `Dockerfile-uv.dockerfile`,
- then rebuilds `local-uv-image:latest` on changes,
- then rebuilds the main `Dockerfile` image,
- then starts the `docker-compose up`, which in turn:
  - starts `postgres:16` container with persistent DB,
  - starts main container connected to it.

It is worth noting that the `uv.lock` and `Dockerfile-uv.dockerfile` changes are checked with checksums, so once the initial build is over, the directory will have checksum files such as `.dockerfile-uv_checksum` and `.uvlock_checksum`.
