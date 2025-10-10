import dataclasses
import enum

from src import utils


class InvalidStudentName(Exception): ...


@dataclasses.dataclass
class Student:
    id: int
    firstname: str
    lastname: str


class SubjectName(enum.StrEnum):
    RU = "Русский язык"
    MATH = "Математика"
    EN = "Английский язык"
    SOCIAL = "Обществознание"
    PHYSICS = "Физика"
    CHEM = "Химия"
    BIO = "Биология"
    GEO = "География"
    LIT = "Литература"
    IT = "Информатика"
    HISTORY = "История"
    DE = "Немецкий язык"
    FR = "Французский язык"
    ES = "Испанский язык"
    CN = "Китайский язык"


@dataclasses.dataclass
class ExamRecord:
    subjectname: SubjectName
    score: int
    studentid: int


def signup_student(firstname: str, lastname: str, studentid: int) -> Student:
    if not utils.is_firstname_correct(firstname):
        raise InvalidStudentName("Имя должно содержать только буквы русского алфавита")
    if not utils.is_lastname_correct(lastname):
        raise InvalidStudentName("Фамилия должна содержать только буквы русского алфавита")
    return Student(firstname=firstname, lastname=lastname, id=studentid)


def add_record(subjectname: SubjectName, score: int, studentid: int) -> ExamRecord:
    return ExamRecord(subjectname, score, studentid)
