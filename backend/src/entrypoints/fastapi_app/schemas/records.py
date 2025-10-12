from typing import Annotated

from pydantic import BaseModel, Field

from src.entrypoints.fastapi_app import enums


class AddRecord(BaseModel):
    subjectname: Annotated[enums.SubjectName, Field(description="Название предмета")]
    score: Annotated[int, Field(description="Кол-во баллов", ge=0, le=100)]
    studentid: Annotated[int, Field(description="ID ученика")]


class RecordAdded(BaseModel):
    msg: str = "Запись добавлена!"


class RecordAlreadyExists(BaseModel):
    msg: str = "Запись по данному предмету уже существует!"


class RecordDoesNotExist(BaseModel):
    msg: str = "Запись по данному предмету не найдена!"


class DeleteRecord(BaseModel):
    subjectname: Annotated[enums.SubjectName, Field(description="Название предмета")]
    studentid: Annotated[int, Field(description="ID ученика")]


class RecordDeleted(BaseModel):
    msg: str = "Запись удалена!"


class UpdateRecordScore(BaseModel):
    subjectname: Annotated[enums.SubjectName, Field(description="Название предмета")]
    new_score: Annotated[int, Field(description="Новое кол-во баллов", ge=0, le=100)]
    studentid: Annotated[int, Field(description="ID ученика")]


class RecordScoreUpdated(BaseModel):
    msg: str = "Баллы обновлены!"
