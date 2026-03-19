from fastapi import APIRouter

from src.queries import queries

router = APIRouter(prefix="/students")


@router.get("/less-than-5-twos")
async def less_than_5_twos() -> list[dict[str, str | int]]:
    result = await queries.query_students_less5twos()
    return [{"full_name": stud.name, "count_twos": stud.count} for stud in result]


@router.get("/more-than-3-twos")
async def more_than_5_twos() -> list[dict[str, str | int]]:
    result = await queries.query_students_more3twos()
    return [{"full_name": stud.name, "count_twos": stud.count} for stud in result]
