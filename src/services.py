from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src import domain
from src.adapters import repository


class StudentAlreadyExists(Exception): ...


def signup(
    firstname: str,
    lastname: str,
    studentid: int,
    student_repo: repository.AbstractStudentRepository,
    session: Session,
) -> None:
    """
    Регистрация ученика, если ученик уже существует, вызывает исключение.
    """
    try:
        if student_repo.get(studentid):
            raise StudentAlreadyExists("Ученик с таким id уже существует")
    except NoResultFound:
        pass

    new_student = domain.signup_student(firstname, lastname, studentid)
    student_repo.add(new_student)
    session.commit()


def add_record(
    subjectname: domain.SubjectName,
    score: int,
    studentid: int,
    examrecord_repo: repository.AbstractExamRecordRepository,
    session: Session,
) -> int:
    new_record = domain.add_record(subjectname, score, studentid)
    examrecord_repo.add(new_record)
    session.commit()


def list_records(
    studentid: str, examrecord_repo: repository.AbstractExamRecordRepository
) -> dict[str, int]:
    return {r.subjectname: r.score for r in examrecord_repo.list(studentid)}
