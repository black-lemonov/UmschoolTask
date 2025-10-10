from src import services, domain
from src.adapters import repository


def test_signup_returns_not_none_id(session):
    firstname, lastname = "Иван", "Иванов"
    student_repo = repository.SQLAlchemyStudentRepository(session)
    id_from_service = services.signup(
        firstname, lastname, student_repo, session
    )
    assert id_from_service is not None
    

def test_add_record_returns_not_none_id(session):
    subject, score, student = "RU", 80, 1
    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    id_from_service = services.add_record(
        domain.SubjectName.RU, score, student, record_repo, session
    )
    assert id_from_service is not None


def test_list_records_returns_existing_values(session):
    record_repo = repository.SQLAlchemyExamRecordRepository(session)
    records = [
        domain.ExamRecord(subjectname=domain.SubjectName.RU, score=40, studentid=1),
        domain.ExamRecord(subjectname=domain.SubjectName.EN, score=60, studentid=1),
        domain.ExamRecord(subjectname=domain.SubjectName.RU, score=30, studentid=2),
    ]
    for record in records:
        record_repo.add(record)
    
    expected_pairs = {
        r.subjectname: r.score for r in records if r.studentid == 1
    }
    assert services.list_records(1, record_repo) == expected_pairs
