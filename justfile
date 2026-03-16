# https://just.systems
set dotenv-load

default:
    just --list

watch:
    uv run uvicorn main:app --reload --log-level=debug

insert:
    curl -i \
        -X POST \
        -H "Content-Type: multipart/form-data" \
        -F "file=@./students_grades.csv" \
        http://localhost:8000/upload-grades

test:
    @echo ""
    curl -i \
        -X GET \
        http://localhost:8000/students/more-than-3-twos

    @echo ""
    curl -i \
        -X GET \
        http://localhost:8000/students/less-than-5-twos
