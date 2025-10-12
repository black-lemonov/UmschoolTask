from typing import Annotated

from fastapi import APIRouter, Response, status, Query

from src.entrypoints.fastapi_app import deps
from src.entrypoints.fastapi_app.schemas import records as schemas
from src.entrypoints.fastapi_app.schemas import student as student_schemas
from src.adapters import repository
from src import services


router = APIRouter(tags=["Предметы и баллы ✍️"])


@router.post(
    "/records",
    summary="Добавить баллы по предмету",
    responses={
        200: {
            "description": "Запись успешно добавлена",
            "model": schemas.RecordAdded,
        },
        400: {
            "description": "Запись уже существует",
            "model": schemas.RecordAlreadyExists,
        },
        401: {
            "description": "Ученик не найден",
            "model": student_schemas.StudentDoesNotExist,
        },
    },
)
async def add_record(
    examrecord: schemas.AddRecord, session: deps.SessionDep, response: Response
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
    except services.RecordAlreadyExists:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return schemas.RecordAlreadyExists()
    except services.StudentDoesNotExist:
        response.status_code = 401
        return student_schemas.StudentDoesNotExist()

    return schemas.RecordAdded()


@router.delete(
    "/records",
    summary="Удалить запись по предмету",
    responses={
        200: {
            "description": "Запись успешно удалена",
            "model": schemas.RecordDeleted,
        },
        404: {
            "description": "Запись не найдена",
            "model": schemas.RecordDoesNotExist,
        },
    },
)
async def delete_record(
    record: schemas.DeleteRecord, session: deps.SessionDep, response: Response
):
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    try:
        await services.delete_record(
            record.subjectname, record.studentid, records_repo, session
        )
    except services.RecordDoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return schemas.RecordDoesNotExist()

    return schemas.RecordDeleted()


@router.patch(
    "/records",
    summary="Изменить баллы по предмету",
    responses={
        200: {
            "description": "Баллы успешно обновлены",
            "model": schemas.RecordScoreUpdated,
        },
        401: {
            "description": "Ученик не найден",
            "model": student_schemas.StudentDoesNotExist,
        },
        404: {
            "description": "Запись не найдена",
            "model": schemas.RecordDoesNotExist,
        },
    },
)
async def update_record_score(
    record: schemas.UpdateRecordScore, session: deps.SessionDep, response: Response
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
    except services.RecordDoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return schemas.RecordDoesNotExist()

    return schemas.RecordScoreUpdated()


@router.get(
    "/scores",
    summary="Получить все предметы с баллами ученика",
    responses={
        200: {"description": "Список записей успешно получен", "model": dict[str, int]},
        401: {
            "description": "Ученик не найден",
            "model": student_schemas.StudentDoesNotExist,
        },
    },
)
async def list_records(
    studentid: Annotated[int, Query(description="ID ученика")],
    session: deps.SessionDep,
    response: Response,
):
    student_repo = repository.SQLAlchemyStudentRepository(session)

    try:
        await services.signin(studentid, student_repo)
    except services.StudentDoesNotExist:
        response.status_code = 401
        return student_schemas.StudentDoesNotExist()

    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    return await services.list_records(studentid, records_repo)
