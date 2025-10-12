from typing import Annotated

from pydantic import BaseModel, Field

from src.entrypoints.fastapi_app import enums


class StudentName(BaseModel):
    firstname: Annotated[
        str,
        Field(examples=["Иван"], pattern=r"^[А-Яа-яЁё]+$", description="Имя ученика"),
    ]
    lastname: Annotated[
        str,
        Field(
            examples=["Иванов"],
            pattern=r"^[А-Яа-яЁё]+(-[А-Яа-яЁё]+)*$",
            description="Фамилия ученика",
        ),
    ]


class SignUpStudent(StudentName):
    studentid: Annotated[int, Field(description="ID ученика")]


class SignInStudent(BaseModel):
    studentid: Annotated[int, Field(description="ID ученика")]


class UpdateStudent(StudentName):
    studentid: Annotated[int, Field(description="ID ученика")]


class AddExamRecord(BaseModel):
    subjectname: Annotated[enums.SubjectName, Field(description="Название предмета")]
    score: Annotated[int, Field(description="Кол-во баллов", ge=0, le=100)]
    studentid: Annotated[int, Field(description="ID ученика")]


class UpdateRecordScore(BaseModel):
    subjectname: Annotated[enums.SubjectName, Field(description="Название предмета")]
    new_score: Annotated[int, Field(description="Новое кол-во баллов", ge=0, le=100)]
    studentid: Annotated[int, Field(description="ID ученика")]


class DeleteRecord(BaseModel):
    subjectname: Annotated[enums.SubjectName, Field(description="Название предмета")]
    studentid: Annotated[int, Field(description="ID ученика")]


class SuccessMessageResponse(BaseModel):
    msg: Annotated[
        str, Field(description="Описание ответа", examples=["Операция выполнена"])
    ]


class ErrorMessageResponse(BaseModel):
    msg: Annotated[
        str, Field(description="Описание ошибки", examples=["Сообщение ошибки"])
    ]
