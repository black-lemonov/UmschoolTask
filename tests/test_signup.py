import pytest

from src import domain


def test_signup_w_correct_firstname_and_lastname():
    correct_firstname, correct_lastname, id = "Иван", "Иванович", 1
    expected_student = domain.Student(firstname=correct_firstname, lastname=correct_lastname, id=id)
    assert domain.signup_student(correct_firstname, correct_lastname, id) == expected_student


def test_try_to_signup_w_alphanum_firstname_and_lastname():
    alphanum_firstname, alphanum_lastname, id = "Иван2004", "Иванович2003rus", 1
    with pytest.raises(domain.InvalidStudentName):
        domain.signup_student(alphanum_firstname, alphanum_lastname, id)
    

def test_signup_w_double_lastname():
    correct_firstname, double_lastname, id = "Иван", "Иванович-Петрович", 1
    student_w_double_lastname = domain.Student(firstname=correct_firstname, lastname=double_lastname, id=id)
    assert domain.signup_student(correct_firstname, double_lastname, id) == student_w_double_lastname
    