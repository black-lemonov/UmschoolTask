import abc

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import domain


class AbstractStudentRepository(abc.ABC):
    @abc.abstractmethod
    async def get(self, id: int) -> domain.Student: ...

    @abc.abstractmethod
    def add(self, student: domain.Student) -> None: ...


class AbstractExamRecordRepository(abc.ABC):
    @abc.abstractmethod
    async def get(self, subjectname: domain.SubjectName, studentid: int) -> domain.ExamRecord: ...

    @abc.abstractmethod
    async def list(self, studentid: int) -> list[domain.ExamRecord]: ...

    @abc.abstractmethod
    def add(self, examrecord: domain.ExamRecord) -> None: ...

    @abc.abstractmethod
    async def delete(self, examrecord: domain.ExamRecord) -> None: ...


class SQLAlchemyStudentRepository(AbstractStudentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> domain.Student:
        result = await self.session.execute(select(domain.Student).filter_by(id=id))
        return result.scalars().one()
    
    def add(self, student: domain.Student) -> None:
        self.session.add(student)


class SQLAlchemyExamRecordRepository(AbstractExamRecordRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, subjectname: domain.SubjectName, studentid: int) -> domain.ExamRecord:
        result = await self.session.execute(select(domain.ExamRecord).filter_by(subjectname=subjectname, studentid=studentid))
        return result.scalars().one()
    
    def add(self, examrecord: domain.ExamRecord) -> None:
        self.session.add(examrecord)
    
    async def list(self, studentid: int) -> list[domain.ExamRecord]:
        result = await self.session.execute(select(domain.ExamRecord).filter_by(studentid=studentid))
        return result.scalars().all()
    
    async def delete(self, examrecord: domain.ExamRecord) -> None:
        await self.session.delete(examrecord)
