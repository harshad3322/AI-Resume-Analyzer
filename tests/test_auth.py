# tests/test_auth.py

from app import app

def test_login_page_loads():

    client = app.test_client()

    response = client.get(
        "/login"
    )

    assert response.status_code == 200