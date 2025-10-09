import pytest
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
            "INSERT INTO examrecords (id, subjectname, score, studentid) VALUES (:id, :subjectname, :score, :studentid)"
        ),
        [
            dict(id=1, subjectname="RU", score=90, studentid=1),
            dict(id=2, subjectname="MATH", score=85, studentid=1),
            dict(id=3, subjectname="EN", score=70, studentid=1),
            dict(id=4, subjectname="RU", score=98, studentid=2),
        ],
    )

    expected_records = [
        domain.ExamRecord(id=1, subjectname=domain.SubjectName.RU, score=90, studentid=1),
        domain.ExamRecord(id=2, subjectname=domain.SubjectName.MATH, score=85, studentid=1),
        domain.ExamRecord(id=3, subjectname=domain.SubjectName.EN, score=70, studentid=1),
    ]

    assert session.query(domain.ExamRecord).filter(domain.ExamRecord.studentid==1).all() == expected_records
