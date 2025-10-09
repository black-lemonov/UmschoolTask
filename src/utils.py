import re


def is_firstname_correct(firstname: str) -> bool:
    firstname_pattern = r'^[А-Яа-яЁё]+$'
    return bool(re.match(firstname_pattern, firstname))


def is_lastname_correct(lastname: str) -> bool:
    lastname_pattern = r'^[А-Яа-яЁё]+(-[А-Яа-яЁё]+)*$'
    return bool(re.match(lastname_pattern, lastname))
