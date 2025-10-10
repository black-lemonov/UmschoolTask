from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, APIRouter, Body, Query, HTTPException, status

from src.config import get_postgres_url
from src.adapters.orm import start_mappers
from src.adapters import repository
from src import services
from src.entrypoints.fastapi_app import enums


app = FastAPI()
auth_router = APIRouter(tags=["Вход/Регистрация"])
scores_router = APIRouter(tags=["Управление результатами"])


engine = create_engine(get_postgres_url())
start_mappers()
get_session = sessionmaker(bind=engine)


@auth_router.post("/signup", summary="Создать запись ученика")
def signup(
    firstname: Annotated[str, Body()],
    lastname: Annotated[str, Body()],
    studentid: Annotated[int, Body()],
):
    session = get_session()
    student_repo = repository.SQLAlchemyStudentRepository(session)
    try:
        services.signup(firstname, lastname, studentid, student_repo, session)
    except services.StudentAlreadyExists as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"msg": "Запись ученика создана"}


@scores_router.post("/scores", summary="Добавить баллы по предмету")
def add_score(
    subjectname: Annotated[enums.SubjectName, Query(description="название предмета")],
    score: Annotated[int, Query(description="кол-во баллов")],
    studentid: Annotated[int, Query(description="id ученика")],
):
    session = get_session()
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    services.add_record(subjectname, score, studentid, records_repo, session)
    return {"msg": "Запись успешно добавлена"}


@scores_router.get("/scores", summary="Получить все предметы с баллами ученика")
def list_records(
    studentid: Annotated[int, Query(description="id ученика")],
):
    session = get_session()
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    return services.list_records(studentid, records_repo)


app.include_router(auth_router)
app.include_router(scores_router)
