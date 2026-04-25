import pytest
from movai import create_app


@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"WHILE DESIGNING THIS SITE" in response.data


def test_invalid_method(client):
    response = client.post("/home")
    assert response.status_code == 405
