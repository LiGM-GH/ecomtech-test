from datetime import datetime
from fastapi import FastAPI, UploadFile
from fastapi import File

import logging
import csv

from models.mark import Mark
from src import queries

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def root():
    return {"whatever": "Whatever with big W"}


@app.post("/upload-grades")
async def upload_grades(file: UploadFile = File(...)):
    logger.debug(f"{file = }")
    reader = csv.reader(map(lambda x: x.decode(), file.file.readlines()), delimiter=";")
    next(reader)

    marks = map(
        lambda line: Mark(
            name=line[2],
            creation_date=datetime.strptime(line[0], "%d.%m.%Y"),
            value=int(line[3]),
        ),
        reader,
    )

    insertion_result = await queries.insert_students(marks)

    logger.debug(f"{insertion_result.rows_added = }")
    logger.debug(f"{insertion_result.students = }")

    return {
        "status": "ok",
        "records_loaded": insertion_result.rows_added,
        "students": insertion_result.students,
    }


@app.get("/students/more-than-3-twos")
async def get_students_more3twos() -> list[dict[str, str | int]]:
    result = await queries.query_students_more3twos()

    return [{"full_name": stud.name, "count_twos": stud.count} for stud in result]


@app.get("/students/less-than-5-twos")
async def get_students_less5twos() -> list[dict[str, str | int]]:
    result = await queries.query_students_less5twos()
    return [{"full_name": stud.name, "count_twos": stud.count} for stud in result]
