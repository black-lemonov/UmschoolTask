from sqlalchemy.orm import Session

from src import repository, domain


def signup(firstname: str, lastname: str, student_repo: repository.AbstractStudentRepository, session: Session) -> int:
    new_student = domain.signup_student(firstname, lastname)
    student_repo.add(new_student)
    session.commit()
    return new_student.id


def add_record(subjectname: str, score: int, studentid: int, examrecord_repo: repository.AbstractExamRecordRepository, session: Session) -> int:
    new_record = domain.add_record(subjectname, score, studentid)
    examrecord_repo.add(new_record)
    session.commit()
    return new_record.id


def list_records(studentid: str, examrecord_repo: repository.AbstractExamRecordRepository) -> dict[str, int]:
    return {r.subjectname: r.score for r in examrecord_repo.list(studentid)}
