from collections.abc import Iterable
from dataclasses import dataclass
import logging
from os import getenv
from typing import cast

from psycopg_pool import AsyncConnectionPool

from models.mark import Mark

logger = logging.getLogger(__name__)

conninfo = getenv("DB_CONN")

if not conninfo:
    logger.critical(
        "DB_CONN variable must be present with the Postgres connection info string"
    )
    exit(1)

pool = AsyncConnectionPool(conninfo=conninfo)


@dataclass
class StudentsInsertionResult:
    rows_added: int
    students: int


@dataclass
class StudentMarkCount:
    name: str
    count: int


async def insert_students(marks: Iterable[Mark]) -> StudentsInsertionResult:
    """
    Insert students into the database.
    """

    async with pool.connection() as conn:
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

        await conn.commit()
        return StudentsInsertionResult(rows_added=rows_added, students=students_count)


async def query_students_more3twos() -> Iterable[StudentMarkCount]:
    """
    Finds the students in the database
    that have more than 3 marks "2"
    and returns their names alongside with their "2" mark count.
    """

    async with pool.connection() as conn:
        cur = await conn.execute("""
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
        """)

        result = cast(list[list[str]], await cur.fetchall())
        logger.debug(f"{result = }")

        result = (StudentMarkCount(name=row[1], count=int(row[0])) for row in result)

        return result


async def query_students_less5twos() -> Iterable[StudentMarkCount]:
    """
    Finds the students in the database
    that have less than 5 marks "2"
    and returns their names alongside with their "2" mark count.
    """

    async with pool.connection() as conn:
        cur = await conn.execute("""
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
        """)

        result: list[list[str]] = await cur.fetchall()
        logger.debug(f"{result = }")
        return (StudentMarkCount(name=row[1], count=int(row[0])) for row in result)
