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
    def get(self, subjectname: domain.SubjectName, studentid: int) -> domain.ExamRecord: ...

    @abc.abstractmethod
    def list(self, studentid: int) -> list[domain.ExamRecord]: ...

    @abc.abstractmethod
    def add(self, examrecord: domain.ExamRecord) -> None: ...

    @abc.abstractmethod
    def delete(self, examrecord: domain.ExamRecord) -> None: ...


class SQLAlchemyStudentRepository(AbstractStudentRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get(self, id: int) -> domain.Student:
        return self.session.query(domain.Student).filter_by(id=id).one()
    
    def add(self, student: domain.Student) -> None:
        self.session.add(student)


class SQLAlchemyExamRecordRepository(AbstractExamRecordRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get(self, subjectname: domain.SubjectName, studentid: int) -> domain.ExamRecord:
        return self.session.query(domain.ExamRecord).filter_by(subjectname=subjectname, studentid=studentid).one()
    
    def add(self, examrecord: domain.ExamRecord) -> None:
        self.session.add(examrecord)
    
    def list(self, studentid: int) -> list[domain.ExamRecord]:
        return self.session.query(domain.ExamRecord).filter_by(studentid=studentid).all()
    
    def delete(self, examrecord: domain.ExamRecord) -> None:
        self.session.delete(examrecord)
