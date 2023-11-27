import pytest
from core import app


@pytest.fixture()
def my_app():
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(my_app):
    return my_app.test_client()


@pytest.fixture()
def runner(my_app):
    return my_app.test_cli_runner()


def test_request_example(client):
    # response = client.get("/posts")
    assert True  # b"<h2>Hello, World!</h2>" in response.data


def test_register_user(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "flask@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    token = response.json['access_token']
    assert response.status_code == 200
