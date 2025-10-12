import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import domain
from src.adapters import repository


@pytest.mark.asyncio
async def test_add_student_saves_data(session: AsyncSession):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    added_student = domain.Student(1, "Иван", "Иванов")
    student_repo.add(added_student)

    selected_student = (await session.execute(select(domain.Student))).scalar_one()
    assert added_student == selected_student


@pytest.mark.asyncio
async def test_add_examrecord_saves_data(session: AsyncSession):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    added_student = domain.Student(1, "Иван", "Иванов")
    student_repo.add(added_student)

    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    added_record = domain.ExamRecord("Русский язык", 90, 1)
    records_repo.add(added_record)

    selected_record = (await session.execute(select(domain.ExamRecord))).scalar_one()
    assert added_record == selected_record


@pytest.mark.asyncio
async def test_list_records_by_studentid_returns_only_correct_records(
    session: AsyncSession,
):
    student_repo = repository.SQLAlchemyStudentRepository(session)
    student_1 = domain.Student(1, "Иван", "Иванов")
    student_2 = domain.Student(2, "Иван", "Иванов")
    student_repo.add(student_1)
    student_repo.add(student_2)

    records_repo = repository.SQLAlchemyExamRecordRepository(session)
    all_records = [
        domain.ExamRecord("Русский язык", 90, 1),
        domain.ExamRecord("Математика", 85, 1),
        domain.ExamRecord("Химия", 78, 2),
        domain.ExamRecord("Биология", 88, 2),
    ]
    student1_records = [
        domain.ExamRecord("Русский язык", 90, 1),
        domain.ExamRecord("Математика", 85, 1),
    ]
    for record in all_records:
        records_repo.add(record)

    student1_records_from_repo = await records_repo.list(studentid=1)
    assert student1_records == student1_records_from_repo
