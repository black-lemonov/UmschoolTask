import pytest

from src import domain


def test_signup_w_correct_firstname_and_lastname():
    correct_firstname, correct_lastname = "Иван", "Иванович"
    expected_student = domain.Student(correct_firstname, correct_lastname)
    assert domain.signup_student(correct_firstname, correct_lastname) == expected_student


def test_try_to_signup_w_alphanum_firstname_and_lastname():
    alphanum_firstname, alphanum_lastname = "Иван2004", "Иванович2003rus"
    with pytest.raises(domain.InvalidStudentName):
        domain.signup_student(alphanum_firstname, alphanum_lastname)
    

def test_signup_w_double_lastname():
    correct_firstname, double_lastname = "Иван", "Иванович-Петрович" 
    student_w_double_lastname = domain.Student(correct_firstname, double_lastname)
    assert domain.signup_student(correct_firstname, double_lastname) == student_w_double_lastname
    