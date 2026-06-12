# tests/test_email.py

import re
from app import EMAIL_REGEX

def test_valid_email():

    assert re.match(
        EMAIL_REGEX,
        "user@gmail.com"
    )

def test_invalid_email():

    assert not re.match(
        EMAIL_REGEX,
        "invalid-email"
    )