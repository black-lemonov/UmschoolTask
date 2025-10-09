from src import repository, domain


def test_add_student_saves_data(session):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    added_student = domain.Student("Иван", "Иванов")
    student_repo.add(added_student)
    [selected_student] = session.query(domain.Student).all()
    assert added_student == selected_student


def test_add_examrecord_saves_data(session):
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    added_record = domain.ExamRecord("Русский язык", 90, 1)
    records_repo.add(added_record)
    [selected_record] = session.query(domain.ExamRecord).all()
    assert added_record == selected_record


def test_list_records_by_studentid_returns_only_correct_records(session):
    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    all_records = [
        domain.ExamRecord("Русский язык", 90, 1),
        domain.ExamRecord("Математика", 85, 1),
        domain.ExamRecord("Химия", 78, 3),
        domain.ExamRecord("Биология", 88, 2),
    ]
    student1_records = [
        domain.ExamRecord("Русский язык", 90, 1),
        domain.ExamRecord("Математика", 85, 1),
    ]
    for record in all_records:
        records_repo.add(record)
    
    student1_records_from_repo = records_repo.list(studentid=1)
    assert student1_records == student1_records_from_repo
