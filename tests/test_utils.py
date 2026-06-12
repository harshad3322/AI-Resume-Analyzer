# tests/test_utils.py

from utils import validate_password

def test_valid_password():
    assert validate_password(
        "Resume@123"
    ) is True

def test_short_password():
    assert validate_password(
        "Ab1!"
    ) is False

def test_missing_uppercase():
    assert validate_password(
        "resume@123"
    ) is False

def test_missing_number():
    assert validate_password(
        "Resume@abc"
    ) is False