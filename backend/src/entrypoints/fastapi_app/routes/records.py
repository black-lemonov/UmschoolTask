from typing import Annotated

from fastapi import APIRouter, Response, status, Query

from src.entrypoints.fastapi_app import schemas, deps
from src.adapters import repository
from src import services


router = APIRouter(tags=["Предметы и баллы ✍️"])


@router.post(
    "/records",
    summary="Добавить баллы по предмету",
    responses={
        200: {
            "description": "Запись успешно добавлена",
            "model": schemas.SuccessMessageResponse,
        },
        400: {
            "description": "Запись уже существует",
            "model": schemas.ErrorMessageResponse,
        },
        401: {"description": "Ученик не найден", "model": schemas.ErrorMessageResponse},
    },
)
async def add_record(
    examrecord: schemas.AddExamRecord, session: deps.SessionDep, response: Response
):
    student_repo = repository.SQLAlchemyStudentRepository(session)

    try:
        await services.signin(examrecord.studentid, student_repo)
    except services.StudentDoesNotExist as e:
        response.status_code = 401
        return {"msg": str(e)}

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
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": str(e)}
    return {"msg": "Запись успешно добавлена"}


@router.delete(
    "/records",
    summary="Удалить запись по предмету",
    responses={
        200: {
            "description": "Запись успешно удалена",
            "model": schemas.SuccessMessageResponse,
        },
        401: {"description": "Ученик не найден", "model": schemas.ErrorMessageResponse},
        404: {
            "description": "Запись не найдена",
            "model": schemas.ErrorMessageResponse,
        },
    },
)
async def delete_record(
    record: schemas.DeleteRecord, session: deps.SessionDep, response: Response
):
    student_repo = repository.SQLAlchemyStudentRepository(session)

    try:
        await services.signin(record.studentid, student_repo)
    except services.StudentDoesNotExist as e:
        response.status_code = 401
        return {"msg": str(e)}
    
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    try:
        await services.delete_record(
            record.subjectname, record.studentid, records_repo, session
        )
    except services.RecordDoesNotExist as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": str(e)}
    return {"msg": "Запись успешно удалена"}


@router.patch(
    "/records",
    summary="Изменить баллы по предмету",
    responses={
        200: {
            "description": "Баллы успешно обновлены",
            "model": schemas.SuccessMessageResponse,
        },
        401: {"description": "Ученик не найден", "model": schemas.ErrorMessageResponse},
        404: {
            "description": "Запись не найдена",
            "model": schemas.ErrorMessageResponse,
        },
    },
)
async def update_record_score(
    record: schemas.UpdateRecordScore, session: deps.SessionDep, response: Response
):
    student_repo = repository.SQLAlchemyStudentRepository(session)

    try:
        await services.signin(record.studentid, student_repo)
    except services.StudentDoesNotExist as e:
        response.status_code = 401
        return {"msg": str(e)}
    
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
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": str(e)}
    return {"msg": "Баллы успешно обновлены"}


@router.get(
    "/scores",
    summary="Получить все предметы с баллами ученика",
    responses={
        200: {"description": "Список записей успешно получен", "model": dict[str, int]},
        401: {"description": "Ученик не найден", "model": schemas.ErrorMessageResponse},
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
    except services.StudentDoesNotExist as e:
        response.status_code = 401
        return {"msg": str(e)}

    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    return await services.list_records(studentid, records_repo)
