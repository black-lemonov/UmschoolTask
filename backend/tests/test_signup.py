from src import domain


def test_signup_w_correct_firstname_and_lastname():
    correct_firstname, correct_lastname, id = "Иван", "Иванович", 1
    expected_student = domain.Student(
        firstname=correct_firstname, lastname=correct_lastname, id=id
    )
    assert (
        domain.signup_student(correct_firstname, correct_lastname, id)
        == expected_student
    )
