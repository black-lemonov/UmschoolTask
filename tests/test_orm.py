from sqlalchemy import text

from src import domain


def test_select_returns_students(session):
    session.execute(
        text(
            "INSERT INTO students (id, firstname, lastname) VALUES (:id, :firstname, :lastname)"
        ),
        [
            dict(id=1, firstname="Иван", lastname="Иванов"),
            dict(id=2, firstname="Денис", lastname="Денисов"),
            dict(id=3, firstname="Андрей", lastname="Андреев"),
        ],
    )

    expected_students = [
        domain.Student(id=1, firstname="Иван", lastname="Иванов"),
        domain.Student(id=2, firstname="Денис", lastname="Денисов"),
        domain.Student(id=3, firstname="Андрей", lastname="Андреев"),
    ]

    assert session.query(domain.Student).all() == expected_students


def test_select_examrecords_by_student_returns_examrecords(session):
    session.execute(
        text(
            "INSERT INTO students (id, firstname, lastname) VALUES (:id, :firstname, :lastname)"
        ),
        [
            dict(id=1, firstname="Иван", lastname="Иванов"),
            dict(id=2, firstname="Петр", lastname="Петров"),
        ],
    )
    session.execute(
        text(
            "INSERT INTO examrecords (subjectname, score, studentid) VALUES (:subjectname, :score, :studentid)"
        ),
        [
            dict(subjectname="RU", score=90, studentid=1),
            dict(subjectname="MATH", score=85, studentid=1),
            dict(subjectname="EN", score=70, studentid=1),
            dict(subjectname="RU", score=98, studentid=2),
        ],
    )

    expected_records = [
        domain.ExamRecord(subjectname=domain.SubjectName.RU, score=90, studentid=1),
        domain.ExamRecord(subjectname=domain.SubjectName.MATH, score=85, studentid=1),
        domain.ExamRecord(subjectname=domain.SubjectName.EN, score=70, studentid=1),
    ]

    assert session.query(domain.ExamRecord).filter(domain.ExamRecord.studentid==1).all() == expected_records
