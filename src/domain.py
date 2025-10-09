import dataclasses

from src import utils

class InvalidStudentName(Exception): ...


@dataclasses.dataclass(frozen=True)
class Student:
    firstname: str
    lastname: str

@dataclasses.dataclass(frozen=True)
class ExamSubject:
    title: str
    score: int


def signup_student(firstname: str, lastname: str) -> Student:
    if not utils.is_firstname_correct(firstname):
        raise InvalidStudentName("Имя должно содержать только буквы")
    if not utils.is_lastname_correct(lastname):
        raise InvalidStudentName("Фамилия должна содержать только буквы")
    return Student(firstname, lastname)
