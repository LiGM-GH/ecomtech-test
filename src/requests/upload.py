import csv
from datetime import datetime
import logging
from fastapi import APIRouter, File, UploadFile

from src.models.mark import Mark
from src.queries import queries

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload-grades")
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
