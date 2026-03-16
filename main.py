from datetime import datetime
from os import getenv
from fastapi import FastAPI, UploadFile
from fastapi import File
from psycopg_pool import AsyncConnectionPool

import logging
import csv

from models.mark import Mark

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

conninfo = getenv("DB_CONN")

if not conninfo:
    logger.critical(
        "DB_CONN variable must be present with the Postgres connection info string"
    )
    exit(1)

pool = AsyncConnectionPool(conninfo=conninfo)
app = FastAPI()


@app.get("/")
async def root():
    return {"whatever": "Whatever with big W"}


@app.post("/upload-grades")
async def upload_grades(file: UploadFile = File(...)):
    logger.warning(f"{file = }")
    reader = csv.reader(map(lambda x: x.decode(), file.file.readlines()), delimiter=";")
    next(reader)
    rows_added = 0
    students_count = 0

    async with pool.connection() as conn:
        marks: list[Mark] = []
        for line in reader:
            mark = Mark(
                name=line[2],
                creation_date=datetime.strptime(line[0], "%d.%m.%Y"),
                value=int(line[3]),
            )
            marks.append(mark)

        students_count_tuple = await (
            await conn.execute(
                "SELECT COUNT(*) FROM (SELECT DISTINCT (name) FROM marks);"
            )
        ).fetchone()
        students_count_prev = students_count_tuple[0] if students_count_tuple else 0

        async with conn.cursor() as cur:
            await cur.executemany(
                "INSERT INTO marks (name, creation_date, value) VALUES (%(name)s, %(creation_date)s, %(value)s);",
                map(lambda x: x.model_dump(), marks),
            )
            rows_added = cur.rowcount

        students_count_tuple = await (
            await conn.execute(
                "SELECT COUNT(*) FROM (SELECT DISTINCT (name) FROM marks);"
            )
        ).fetchone()
        students_count = students_count_tuple[0] if students_count_tuple else 0
        students_added = students_count - students_count_prev

        await conn.commit()

    logger.debug(f"{rows_added = }")
    logger.debug(f"{students_added = }")

    return {"status": "ok", "records_loaded": rows_added, "students": students_added}


@app.get("/students/more-than-3-twos")
async def count_students_more3twos() -> list[dict[str, str | int]]:
    async with pool.connection() as conn:
        result: list[list[str | int]] = await (await conn.execute("""
            SELECT
                count AS count_twos,
                name AS full_name
            FROM (
                SELECT COUNT(*), name
                FROM marks
                WHERE value = 2
                GROUP BY name
            )
            WHERE count > 3;
            """)).fetchall()
        logger.debug(f"{result = }")

        return list(map(lambda x: {"full_name": x[1], "count_twos": int(x[0])}, result))

@app.get("/students/less-than-5-twos")
async def count_students_less5twos() -> list[dict[str, str | int]]:
    async with pool.connection() as conn:
        result: list[list[str | int]] = await (await conn.execute("""
            SELECT
                count AS count_twos,
                name AS full_name
            FROM (
                SELECT COUNT(*), name
                FROM marks
                WHERE value = 2
                GROUP BY name
            )
            WHERE count < 5;
            """)).fetchall()
        logger.debug(f"{result = }")

        return list(map(lambda x: {"full_name": x[1], "count_twos": int(x[0])}, result))
