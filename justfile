# https://just.systems

default:
    just --list

watch:
    uv run uvicorn main:app --reload
