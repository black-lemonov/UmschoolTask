import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src import domain, services
from src.adapters import repository


@pytest.mark.asyncio
async def test_signup_saves_student_in_db(session: AsyncSession):
    firstname, lastname, studentid = "Иван", "Иванов", 1
    student_repo = repository.SQLAlchemyStudentRepository(session)
    await services.signup(firstname, lastname, studentid, student_repo, session)
    signedup_student = await student_repo.get(studentid)
    assert signedup_student is not None


@pytest.mark.asyncio
async def test_signup_student_with_existing_id_raises_error(session: AsyncSession):
    student_repo = repository.SQLAlchemyStudentRepository(session)

    student1_firstname, student1_lastname, student1_id = "Иван", "Иванов", 1
    await services.signup(
        student1_firstname, student1_lastname, student1_id, student_repo, session
    )

    student2_firstname, student2_lastname, student2_id = "Петр", "Петров", 1

    with pytest.raises(services.StudentAlreadyExists):
        await services.signup(
            student2_firstname, student2_lastname, student2_id, student_repo, session
        )


@pytest.mark.asyncio
async def test_signin_with_existing_student_does_not_raises_error(
    session: AsyncSession,
):
    student_repo = repository.SQLAlchemyStudentRepository(session)

    firstname, lastname, studentid = "Иван", "Иванов", 1

    student_repo.add(domain.Student(studentid, firstname, lastname))

    await services.signin(studentid, student_repo)


@pytest.mark.asyncio
async def test_signin_non_existing_student_raises_error(session: AsyncSession):
    student_repo = repository.SQLAlchemyStudentRepository(session)

    non_existing_student_id = 1

    with pytest.raises(services.StudentDoesNotExist):
        await services.signin(non_existing_student_id, student_repo)


@pytest.mark.asyncio
async def test_update_existing_student_updates_db(session: AsyncSession):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    firstname, lastname, studentid = "Иван", "Иванов", 1

    student_repo.add(domain.Student(studentid, firstname, lastname))
    new_lastname = "Петров"

    await services.update_student(
        firstname, new_lastname, studentid, student_repo, session
    )
    student = await student_repo.get(studentid)
    assert student.lastname == new_lastname


@pytest.mark.asyncio
async def test_update_student_with_non_existing_id_raises_error(session: AsyncSession):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    firstname, lastname, studentid = "Иван", "Иванов", 1

    with pytest.raises(services.StudentDoesNotExist):
        await services.update_student(
            firstname, lastname, studentid, student_repo, session
        )


@pytest.mark.asyncio
async def test_add_record_saves_record_in_db(session: AsyncSession):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    student_repo.add(domain.Student(1, "Иван", "Иванов"))

    subject, score, student = domain.SubjectName.RU, 80, 1
    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    await services.add_record(subject, score, student, record_repo, session)

    added_record = await record_repo.get(subject, student)
    assert added_record is not None


@pytest.mark.asyncio
async def test_add_record_of_non_existing_student_raises_error(session: AsyncSession):
    subject, score, non_exsisting_student = domain.SubjectName.RU, 80, 1
    record_repo = repository.SQLAlchemyExamRecordRepository(session)

    with pytest.raises(services.StudentDoesNotExist):
        await services.add_record(
            subject, score, non_exsisting_student, record_repo, session
        )


@pytest.mark.asyncio
async def test_delete_existing_record_deletes_record_in_db(session: AsyncSession):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    student_repo.add(domain.Student(1, "Иван", "Иванов"))

    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    subject, score, student = domain.SubjectName.RU, 80, 1
    record_repo.add(domain.ExamRecord(subject, score, student))

    await services.delete_record(subject, student, record_repo, session)

    with pytest.raises(NoResultFound):
        await record_repo.get(subject, student)


@pytest.mark.asyncio
async def test_delete_non_existing_record_raises_error(session: AsyncSession):
    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    non_existing_student = 1

    with pytest.raises(services.RecordDoesNotExist):
        await services.delete_record(
            domain.SubjectName.RU, non_existing_student, record_repo, session
        )


@pytest.mark.asyncio
async def test_update_record_score_updates_db(session: AsyncSession):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    student_repo.add(domain.Student(1, "Иван", "Иванов"))

    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    subject, old_score, student = domain.SubjectName.BIO, 80, 1
    record = domain.ExamRecord(subject, old_score, student)
    record_repo.add(record)

    new_score = 100
    await services.update_record_score(
        subject, new_score, student, record_repo, session
    )

    assert record.score == new_score


@pytest.mark.asyncio
async def test_update_non_existing_record_raises_error(session: AsyncSession):
    record_repo = repository.SQLAlchemyExamRecordRepository(session)

    non_existing_subject, non_existing_score, non_existing_student = (
        domain.SubjectName.BIO,
        80,
        1,
    )

    with pytest.raises(services.RecordDoesNotExist):
        await services.update_record_score(
            non_existing_subject,
            non_existing_score,
            non_existing_student,
            record_repo,
            session,
        )


@pytest.mark.asyncio
async def test_list_records_returns_existing_values(session: AsyncSession):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    student_repo.add(domain.Student(1, "Иван", "Иванов"))
    student_repo.add(domain.Student(2, "Петр", "Петров"))

    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    records = [
        domain.ExamRecord(subjectname=domain.SubjectName.RU, score=40, studentid=1),
        domain.ExamRecord(subjectname=domain.SubjectName.EN, score=60, studentid=1),
        domain.ExamRecord(subjectname=domain.SubjectName.RU, score=30, studentid=2),
    ]
    for record in records:
        record_repo.add(record)

    actual_records = await services.list_records(1, record_repo)
    expected_records = {r.subjectname: r.score for r in records if r.studentid == 1}
    assert actual_records == expected_records
