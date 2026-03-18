# https://just.systems

set dotenv-load

docker_image_tag := "local-uv-image:latest"

uv_dockerfile := "Dockerfile-uv.dockerfile"
uv_dockerfile_checksumfile := ".dockerfile-uv_checksum"
uv_lock := "./uv.lock"
uv_lock_checksumfile := ".uvlock_checksum"

# List the tasks
default:
    just --list --list-submodules

# Start the server
watch:
    uv run uvicorn main:app --reload --log-level=debug

# Start the docker
start: update-uv-docker
    docker-compose build --no-cache
    docker-compose up

[script("bash")]
update-uv-docker:
    if \
        [ -f '{{ uv_lock_checksumfile }}' ] \
        && [ -f '{{ uv_lock }}' ] \
        && [ "$(cat '{{ uv_lock_checksumfile }}')" == "$(cksum '{{ uv_lock }}')" ] \
        && [ -f "{{ uv_dockerfile_checksumfile }}" ] \
        && [ -f "{{ uv_dockerfile }}" ] \
        && [ "$(cat '{{ uv_dockerfile_checksumfile }}')" == "$(cksum '{{ uv_dockerfile }}')" ]; \
    then echo "OK"; \
    else \
        echo "CHECKSUMS DIDN'T MATCH" \
        && docker build . --file '{{ uv_dockerfile }}' --tag '{{ docker_image_tag }}' \
        && echo "$(cksum '{{ uv_lock }}')" > '{{ uv_lock_checksumfile }}' \
        && echo "$(cksum '{{ uv_dockerfile }}')" > '{{ uv_dockerfile_checksumfile }}' \
        && echo "WRITTEN CHECKSUMS"; \
    fi

# Stop the docker
stop:
    docker-compose down

# Insert data into the app
insert:
    curl -i \
        -X POST \
        -H "Content-Type: multipart/form-data" \
        -F "file=@./students_grades.csv" \
        http://localhost:8000/upload-grades

# Test the GET requests to the API
test:
    @echo ""
    curl -i \
        -X GET \
        http://localhost:8000/students/more-than-3-twos

    @echo ""
    curl -i \
        -X GET \
        http://localhost:8000/students/less-than-5-twos
