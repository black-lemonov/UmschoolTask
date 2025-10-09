from src import domain


def test_add_correct_record():
    subject, score = "Русский язык", 90
    expected_record = domain.ExamRecord(subjectname=subject, score=score, studentid=1)
    assert domain.add_record(subject, score, 1) == expected_record
