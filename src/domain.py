import dataclasses
import enum


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
    return Student(firstname=firstname, lastname=lastname, id=studentid)


def add_record(subjectname: SubjectName, score: int, studentid: int) -> ExamRecord:
    return ExamRecord(subjectname, score, studentid)
