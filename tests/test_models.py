# tests/test_models.py

from models import User

def test_user_creation():

    user = User(
        email="test@test.com",
        password="hashed"
    )

    assert user.email == "test@test.com"
    assert user.password == "hashed"