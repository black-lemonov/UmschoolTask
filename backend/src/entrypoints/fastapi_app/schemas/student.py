from typing import Annotated

from pydantic import BaseModel, Field


class BaseStudent(BaseModel):
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


class SignUpStudent(BaseStudent):
    studentid: Annotated[int, Field(description="ID ученика")]


class StudentSignedUp(BaseModel):
    msg: str = "Ученик зарегистрирован!"


class StudentAlreadySignedUp(BaseModel):
    msg: str = "Ученик уже зарегистрирован!"


class SignInStudent(BaseModel):
    studentid: Annotated[int, Field(description="ID ученика")]


class StudentSignedIn(BaseModel):
    msg: str = "Вход выполнен!"


class StudentDoesNotExist(BaseModel):
    msg: str = "Ученик не существует!"


class UpdateStudent(BaseStudent):
    studentid: Annotated[int, Field(description="ID ученика")]


class StudentUpdated(BaseModel):
    msg: str = "Данные ученика обновлены!"
