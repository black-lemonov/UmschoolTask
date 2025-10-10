import pytest
from sqlalchemy.exc import NoResultFound

from src import domain, services
from src.adapters import repository


def test_signup_saves_student_in_db(session):
    firstname, lastname, studentid = "Иван", "Иванов", 1
    student_repo = repository.SQLAlchemyStudentRepository(session)
    services.signup(firstname, lastname, studentid, student_repo, session)
    assert student_repo.get(studentid) is not None


def test_signup_student_with_existing_id_raises_error(session):
    student_repo = repository.SQLAlchemyStudentRepository(session)

    student1_firstname, student1_lastname, student1_id = "Иван", "Иванов", 1
    services.signup(
        student1_firstname, student1_lastname, student1_id, student_repo, session
    )

    student2_firstname, student2_lastname, student2_id = "Петр", "Петров", 1

    with pytest.raises(services.StudentAlreadyExists):
        services.signup(
            student2_firstname, student2_lastname, student2_id, student_repo, session
        )


def test_signin_with_existing_student(session):
    student_repo = repository.SQLAlchemyStudentRepository(session)

    firstname, lastname, studentid = "Иван", "Иванов", 1

    student_repo.add(domain.Student(studentid, firstname, lastname))

    services.signin(studentid, student_repo)


def test_signin_non_existing_student_raises_error(session):
    student_repo = repository.SQLAlchemyStudentRepository(session)

    non_existing_student_id = 1

    with pytest.raises(services.StudentDoesNotExist):
        services.signin(non_existing_student_id, student_repo)


def test_update_existing_student_updates_db(session):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    firstname, lastname, studentid = "Иван", "Иванов", 1

    student_repo.add(domain.Student(studentid, firstname, lastname))
    new_lastname = "Петров"

    services.update_student(firstname, new_lastname, studentid, student_repo, session)
    student = student_repo.get(studentid)
    assert student.lastname == new_lastname


def test_update_student_with_non_existing_id_raises_error(session):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    firstname, lastname, studentid = "Иван", "Иванов", 1

    with pytest.raises(services.StudentDoesNotExist):
        services.update_student(firstname, lastname, studentid, student_repo, session)


def test_delete_existing_record_deletes_record_in_db(session):
    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    subject, score, student = domain.SubjectName.RU, 80, 1
    record_repo.add(domain.ExamRecord(subject, score, student))
    services.delete_record(subject, student, record_repo, session)
    with pytest.raises(NoResultFound):
        record_repo.get(subject, student)


def test_delete_non_existing_record_raises_error(session):
    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    non_existing_student = 1

    with pytest.raises(services.RecordDoesNotExist):
        services.delete_record(
            domain.SubjectName.RU, non_existing_student, record_repo, session
        )


def test_update_score_updates_db(session):
    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    subject, old_score, student = domain.SubjectName.BIO, 80, 1
    record = domain.ExamRecord(subject, old_score, student)
    record_repo.add(record)
    new_score = 100
    services.update_record_score(subject, new_score, student, record_repo, session)
    assert record.score == new_score


def test_update_non_existing_record_raises_error(session):
    record_repo = repository.SQLAlchemyExamRecordRepository(session)

    non_existing_subject, non_existing_score, non_existing_student = (
        domain.SubjectName.BIO,
        80,
        1,
    )

    with pytest.raises(services.RecordDoesNotExist):
        services.update_record_score(
            non_existing_subject,
            non_existing_score,
            non_existing_student,
            record_repo,
            session,
        )


def test_add_record_saves_record_in_db(session):
    subject, score, student = domain.SubjectName.RU, 80, 1
    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    services.add_record(subject, score, student, record_repo, session)
    assert record_repo.get(subject, student) is not None


def test_list_records_returns_existing_values(session):
    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    records = [
        domain.ExamRecord(subjectname=domain.SubjectName.RU, score=40, studentid=1),
        domain.ExamRecord(subjectname=domain.SubjectName.EN, score=60, studentid=1),
        domain.ExamRecord(subjectname=domain.SubjectName.RU, score=30, studentid=2),
    ]
    for record in records:
        record_repo.add(record)

    expected_pairs = {r.subjectname: r.score for r in records if r.studentid == 1}
    assert services.list_records(1, record_repo) == expected_pairs
