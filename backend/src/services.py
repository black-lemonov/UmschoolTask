from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src import domain
from src.adapters import repository


class StudentAlreadyExists(Exception): ...


class StudentDoesNotExist(Exception): ...


class RecordAlreadyExists(Exception): ...


class RecordDoesNotExist(Exception): ...


async def signup(
    firstname: str,
    lastname: str,
    studentid: int,
    student_repo: repository.AbstractStudentRepository,
    session: AsyncSession,
) -> None:
    """
    Регистрация ученика, если ученик уже существует, вызывает исключение.
    """
    try:
        if await student_repo.get(studentid):
            raise StudentAlreadyExists("Ученик уже существует")
    except NoResultFound:
        pass

    new_student = domain.signup_student(firstname, lastname, studentid)
    student_repo.add(new_student)
    await session.commit()


async def signin(studentid: int, student_repo: repository.AbstractStudentRepository):
    """
    Вход ученика по id, если ученик не найден вызывает исключение
    """
    try:
        await student_repo.get(studentid)
    except NoResultFound:
        raise StudentDoesNotExist("Ученик не найден")


async def update_student(
    firstname: str,
    lastname: str,
    studentid: int,
    student_repo: repository.AbstractStudentRepository,
    session: AsyncSession,
):
    """
    Установить новые значения для firstname и lastname, если пользователь не найден, вызывает исключение
    """
    try:
        await student_repo.get(studentid)
    except NoResultFound:
        raise StudentDoesNotExist("Ученик не найден")

    student = await student_repo.get(studentid)
    student.firstname = firstname
    student.lastname = lastname

    await session.commit()


async def add_record(
    subjectname: domain.SubjectName,
    score: int,
    studentid: int,
    examrecord_repo: repository.AbstractExamRecordRepository,
    session: AsyncSession,
) -> None:
    """
    Добавление записи о предмете, если запись уже существует, вызывает исключение
    """
    try:
        if await examrecord_repo.get(subjectname, studentid):
            raise RecordAlreadyExists("Запись по такому предмету уже существует")
    except NoResultFound:
        pass

    new_record = domain.add_record(subjectname, score, studentid)
    examrecord_repo.add(new_record)

    await session.commit()


async def delete_record(
    subjectname: domain.SubjectName,
    studentid: int,
    examrecord_repo: repository.AbstractExamRecordRepository,
    session: AsyncSession,
) -> None:
    """
    Удалить запись пользователя о предмете, вызывает ошибку, если предмет не найден
    """
    try:
        record = await examrecord_repo.get(subjectname, studentid)
    except NoResultFound:
        raise RecordDoesNotExist("Запись по данному предмету не найдена")

    await examrecord_repo.delete(record)

    await session.commit()


async def update_record_score(
    subjectname: domain.SubjectName,
    new_score: int,
    studentid: int,
    examrecord_repo: repository.AbstractExamRecordRepository,
    session: AsyncSession,
) -> None:
    """
    Устанавливает новое кол-во баллов для заданного предмета у пользователя, если записи не существует, возвращает исключение
    """
    try:
        record = await examrecord_repo.get(subjectname, studentid)
    except NoResultFound:
        raise RecordDoesNotExist("Запись по данному предмету не найдена")

    record.score = new_score
    await session.commit()


async def list_records(
    studentid: str, examrecord_repo: repository.AbstractExamRecordRepository
) -> dict[str, int]:
    """
    Возвращает все записи о предметах для ученика с заданным id
    """
    records = await examrecord_repo.list(studentid)
    return {r.subjectname: r.score for r in records}
