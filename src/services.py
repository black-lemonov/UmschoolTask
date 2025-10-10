from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src import domain
from src.adapters import repository


class StudentAlreadyExists(Exception): ...


class StudentDoesNotExist(Exception): ...


class RecordAlreadyExists(Exception): ...


class RecordDoesNotExist(Exception): ...


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

    
def signin(studentid: int, student_repo: repository.AbstractStudentRepository):
    """
    Вход ученика по id
    """
    try:
        student_repo.get(studentid)
    except NoResultFound:
        raise StudentDoesNotExist("Ученик с таким id не найден")


def update_student(
    firstname: str,
    lastname: str,
    studentid: int,
    student_repo: repository.AbstractStudentRepository,
    session: Session,
):
    try:
        student_repo.get(studentid)
    except NoResultFound:
        raise StudentDoesNotExist("Ученик с таким id не найден")
    student = student_repo.get(studentid)
    student.firstname = firstname
    student.lastname = lastname
    session.commit()


def add_record(
    subjectname: domain.SubjectName,
    score: int,
    studentid: int,
    examrecord_repo: repository.AbstractExamRecordRepository,
    session: Session,
) -> None:
    """
    Добавление записи о предмете, если запись уже существует, вызывает исключение
    """
    try:
        if examrecord_repo.get(subjectname, studentid):
            raise RecordAlreadyExists("Запись по такому предмету уже существует")
    except NoResultFound:
        pass
    new_record = domain.add_record(subjectname, score, studentid)
    examrecord_repo.add(new_record)
    session.commit()


def delete_record(
    subjectname: domain.SubjectName,
    studentid: int,
    examrecord_repo: repository.AbstractExamRecordRepository,
    session: Session,
) -> None: 
    """
    Удалить запись пользователя о предмете, вызывает ошибку, если предмет не найден
    """
    try:
        record = examrecord_repo.get(subjectname, studentid)
    except NoResultFound:
        raise RecordDoesNotExist("Запись по данному предмету не существует")

    examrecord_repo.delete(record)
    session.commit()


def update_record_score(
    subjectname: domain.SubjectName,
    new_score: int,
    studentid: int,
    examrecord_repo: repository.AbstractExamRecordRepository,
    session: Session,
) -> None:
    """
    Устанавливает новое кол-во баллов для заданного предмета у пользователя, если записи не существует, возвращает исключение
    """
    try:
        record = examrecord_repo.get(subjectname, studentid)
    except NoResultFound:
        raise RecordDoesNotExist("Записи по данному предмету не существует")
    
    record.score = new_score
    session.commit()


def list_records(
    studentid: str, examrecord_repo: repository.AbstractExamRecordRepository
) -> dict[str, int]:
    """
    Возвращает все записи о предметах для ученика с заданным id
    """
    return {r.subjectname: r.score for r in examrecord_repo.list(studentid)}
