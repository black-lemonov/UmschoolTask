import abc

from sqlalchemy.orm import Session

from src import domain


class AbstractStudentRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> domain.Student: ...

    @abc.abstractmethod
    def add(self, student: domain.Student) -> None: ...


class AbstractExamRecordRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> domain.ExamRecord: ...

    @abc.abstractmethod
    def list(self, studentid: int) -> list[domain.ExamRecord]: ...

    @abc.abstractmethod
    def add(self, examrecord: domain.ExamRecord) -> None: ...


class SQLAlchemyStudentRepository(AbstractStudentRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get(self, id: int) -> domain.Student:
        return self.session.query(domain.Student).filter_by(id=id).one()
    
    def add(self, student: domain.Student) -> None:
        return self.session.add(student)


class SQLAlchemyExamRecordRepository(AbstractExamRecordRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get(self, id: int) -> domain.ExamRecord:
        return self.session.query(domain.ExamRecord).filter_by(id=id).one()
    
    def add(self, examrecord: domain.ExamRecord) -> None:
        return self.session.add(examrecord)
    
    def list(self, studentid: int) -> list[domain.ExamRecord]:
        return self.session.query(domain.ExamRecord).filter_by(studentid=studentid).all()
