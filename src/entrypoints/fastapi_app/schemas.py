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
    studentid: Annotated[int, Field(description="id ученика")]


class SignInStudent(BaseModel):
    studentid: Annotated[int, Field(description="id ученика")]


class UpdateStudent(StudentName):
    studentid: Annotated[int, Field(description="id ученика")]


class AddExamRecord(BaseModel):
    subjectname: Annotated[enums.SubjectName, Field(description="название предмета")]
    score: Annotated[int, Field(description="кол-во баллов", ge=0, le=100)]
    studentid: Annotated[int, Field(description="id ученика")]


class UpdateRecordScore(BaseModel):
    subjectname: Annotated[enums.SubjectName, Field(description="название предмета")]
    new_score: Annotated[int, Field(description="новое кол-во баллов", ge=0, le=100)]
    studentid: Annotated[int, Field(description="id ученика")]


class DeleteRecord(BaseModel):
    subjectname: Annotated[enums.SubjectName, Field(description="название предмета")]
    studentid: Annotated[int, Field(description="id ученика")]
