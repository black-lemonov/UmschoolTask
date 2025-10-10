from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, APIRouter, Body, Query

from src.config import get_postgres_url
from src.orm import start_mappers
from src import repository, services


app = FastAPI()
register_router = APIRouter(tags=["Регистрация"])
student_router = APIRouter(tags=["Ученик"])


engine = create_engine(get_postgres_url())
start_mappers()
get_session = sessionmaker(bind=engine)


@register_router.post("/signup", summary="Создать запись ученика")
def signup(
    firstname: Annotated[str, Body()],
    lastname: Annotated[str, Body()],
):
    session = get_session()
    student_repo = repository.SQLAlchemyStudentRepository(session)
    services.signup(firstname, lastname, student_repo, session)
    return {"msg": "Запись ученика создана"}


@student_router.post("/scores", summary="Добавить баллы по предмету")
def add_score(
    subjectname: Annotated[str, Query(description="название предмета")],
    score: Annotated[int, Query(description="кол-во баллов")],
    studentid: Annotated[int, Query(description="id ученика")],
):
    session = get_session()
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    services.add_record(
        subjectname, score, studentid, records_repo, session
    )
    return {"msg": "Запись успешно добавлена"}


@student_router.get("/scores", summary="Получить баллы ученика")
def list_records(
    studentid: Annotated[int, Query(description="id ученика")],
):
    session = get_session()
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    return services.list_records(studentid, records_repo)


app.include_router(register_router)
app.include_router(student_router)