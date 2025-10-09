import dataclasses
import enum

from src import utils


class InvalidStudentName(Exception): ...


@dataclasses.dataclass
class Student:
    id: int = None
    firstname: str = None
    lastname: str = None


class SubjectName(enum.StrEnum):
    RU = "Русский язык"
    MATH = "Математика" 
    EN = "Английский язык"


@dataclasses.dataclass
class ExamRecord:
    id: int = None
    subjectname: SubjectName = None
    score: int = None
    studentid: int = None


def signup_student(firstname: str, lastname: str) -> Student:
    if not utils.is_firstname_correct(firstname):
        raise InvalidStudentName("Имя должно содержать только буквы")
    if not utils.is_lastname_correct(lastname):
        raise InvalidStudentName("Фамилия должна содержать только буквы")
    return Student(firstname=firstname, lastname=lastname)


def add_record(subjectname: SubjectName, score: int, studentid: int) -> ExamRecord:
    return ExamRecord(subjectname=subjectname, score=score, studentid=studentid)
