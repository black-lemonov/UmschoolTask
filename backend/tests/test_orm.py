import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src import domain


@pytest.mark.asyncio
async def test_select_returns_students(session: AsyncSession):
    await session.execute(
        text(
            "INSERT INTO students (id, firstname, lastname) VALUES (:id, :firstname, :lastname)"
        ),
        [
            dict(id=1, firstname="Иван", lastname="Иванов"),
            dict(id=2, firstname="Денис", lastname="Денисов"),
            dict(id=3, firstname="Андрей", lastname="Андреев"),
        ],
    )
    await session.commit()

    result = await session.execute(select(domain.Student))
    students = result.scalars().all()

    expected_students = [
        domain.Student(id=1, firstname="Иван", lastname="Иванов"),
        domain.Student(id=2, firstname="Денис", lastname="Денисов"),
        domain.Student(id=3, firstname="Андрей", lastname="Андреев"),
    ]

    assert students == expected_students


@pytest.mark.asyncio
async def test_select_examrecords_by_student_returns_examrecords(session: AsyncSession):
    await session.execute(
        text(
            "INSERT INTO students (id, firstname, lastname) VALUES (:id, :firstname, :lastname)"
        ),
        [
            dict(id=1, firstname="Иван", lastname="Иванов"),
            dict(id=2, firstname="Петр", lastname="Петров"),
        ],
    )

    await session.execute(
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

    result = await session.execute(select(domain.ExamRecord).filter_by(studentid=1))
    exam_records = result.scalars().all()

    expected_records = [
        domain.ExamRecord(subjectname=domain.SubjectName.RU, score=90, studentid=1),
        domain.ExamRecord(subjectname=domain.SubjectName.MATH, score=85, studentid=1),
        domain.ExamRecord(subjectname=domain.SubjectName.EN, score=70, studentid=1),
    ]

    assert exam_records == expected_records
