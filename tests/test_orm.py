import pytest
from sqlalchemy import text

from src import domain


def test_select_returns_students(session):
    session.execute(
        text(
            "INSERT INTO students (firstname, lastname) VALUES (:firstname, :lastname)"
        ),
        [
            dict(firstname="Иван", lastname="Иванов"),
            dict(firstname="Денис", lastname="Денисов"),
            dict(firstname="Андрей", lastname="Андреев"),
        ],
    )

    expected_students = [
        domain.Student(firstname="Иван", lastname="Иванов"),
        domain.Student(firstname="Денис", lastname="Денисов"),
        domain.Student(firstname="Андрей", lastname="Андреев"),
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
            dict(subjectname="Русский язык", score=90, studentid=1),
            dict(subjectname="Математика", score=85, studentid=1),
            dict(subjectname="Обществознание", score=70, studentid=1),
            dict(subjectname="Английский язык", score=98, studentid=2),
        ],
    )

    expected_records = [
        domain.ExamRecord(subjectname="Русский язык", score=90, studentid=1),
        domain.ExamRecord(subjectname="Математика", score=85, studentid=1),
        domain.ExamRecord(subjectname="Обществознание", score=70, studentid=1),
    ]

    assert session.query(domain.ExamRecord).filter(domain.ExamRecord.studentid==1).all() == expected_records
