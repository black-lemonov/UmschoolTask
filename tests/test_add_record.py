from src import domain


def test_add_correct_record():
    subject, score = "Русский язык", 90
    expected_record = domain.ExamRecord(subject, score)
    assert domain.add_record(subject, score) == expected_record
