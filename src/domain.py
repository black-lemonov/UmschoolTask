import dataclasses

from src import utils


class InvalidStudentName(Exception): ...


@dataclasses.dataclass
class Student:
    id: int = None
    firstname: str = None
    lastname: str = None


@dataclasses.dataclass
class ExamRecord:
    subjectname: str
    score: int
    studentid: int


def signup_student(firstname: str, lastname: str) -> Student:
    if not utils.is_firstname_correct(firstname):
        raise InvalidStudentName("Имя должно содержать только буквы")
    if not utils.is_lastname_correct(lastname):
        raise InvalidStudentName("Фамилия должна содержать только буквы")
    return Student(firstname, lastname)


def add_record(subjectname: str, score: int, studentid: int) -> ExamRecord:
    return ExamRecord(subjectname, score, studentid)
