import pytest

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
