from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from src import services
from src.adapters import repository
from src.entrypoints.fastapi_app import deps, schemas

student_router = APIRouter(tags=["Профиль"])
records_router = APIRouter(tags=["Управление результатами"])


@student_router.post("/signup", summary="Создать запись ученика")
async def signup(
    student: schemas.SignUpStudent,
    session: deps.SessionDep,
):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    try:
        await services.signup(
            student.firstname,
            student.lastname,
            student.studentid,
            student_repo,
            session,
        )
    except services.StudentAlreadyExists as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"msg": "Запись ученика создана"}


@student_router.post("/signin", summary="Войти по id")
async def signin(student: schemas.SignInStudent, session: deps.SessionDep):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    try:
        await services.signin(student.studentid, student_repo)
    except services.StudentDoesNotExist as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {"msg": "Вход выполнен"}


@student_router.put("/student", summary="Изменить личные данные пользователя")
async def update_student(student: schemas.UpdateStudent, session: deps.SessionDep):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    try:
        await services.update_student(
            student.firstname,
            student.lastname,
            student.studentid,
            student_repo,
            session,
        )
    except services.StudentDoesNotExist as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {"msg": "Информация обновлена"}


@records_router.post("/records", summary="Добавить баллы по предмету")
async def add_record(
    examrecord: schemas.AddExamRecord,
    session: deps.SessionDep,
):
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    try:
        await services.add_record(
            examrecord.subjectname,
            examrecord.score,
            examrecord.studentid,
            records_repo,
            session,
        )
    except services.RecordAlreadyExists as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"msg": "Запись успешно добавлена"}


@records_router.delete("/records", summary="Удалить запись по предмету")
async def delete_record(record: schemas.DeleteRecord, session: deps.SessionDep):
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    try:
        await services.delete_record(
            record.subjectname, record.studentid, records_repo, session
        )
    except services.RecordDoesNotExist as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {"msg": "Запись успешно удалена"}


@records_router.patch("/records", summary="Изменить баллы по предмету")
async def update_record_score(
    record: schemas.UpdateRecordScore, session: deps.SessionDep
):
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    try:
        await services.update_record_score(
            record.subjectname,
            record.new_score,
            record.studentid,
            records_repo,
            session,
        )
    except services.RecordDoesNotExist as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {"msg": "Баллы успешно обновлены!"}


@records_router.get("/scores", summary="Получить все предметы с баллами ученика")
async def list_records(
    studentid: Annotated[int, Query(description="id ученика")], session: deps.SessionDep
):
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    return await services.list_records(studentid, records_repo)
