from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry, relationship

from src import domain


mapper_registry = registry()


students = Table(
    "students",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("firstname", String(50)),
    Column("lastname", String(50)),
)

examrecords = Table(
    "examrecords",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("subjectname", String(50)),
    Column("score", Integer),
    Column("studentid", Integer, ForeignKey("students.id")),
)


def start_mappers():
    mapper_registry.map_imperatively(
        domain.Student,
        students,
        properties={
            "exam_records": relationship(domain.ExamRecord, back_populates="student")
        }
    )
    mapper_registry.map_imperatively(
        domain.ExamRecord,
        examrecords,
        properties={
            "student": relationship(domain.Student, back_populates="exam_records")
        }
    )
