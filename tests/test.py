from datetime import date

import pytest

from core import app
from DB import data_base


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


def test_register_user(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "a@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    # noinspection PyBroadException
    try:
        data_base.delete_user("a@flask.flask")
    except Exception:
        pass
    print(response.data.decode('utf-8'))
    assert response.status_code == 200


def test_register_user_short_nick(client):
    response = client.post("/register", json={
        "nickname": "g",
        "email": "flask@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    assert response.status_code == 400
    assert "Слишком короткий Ник!" in response.data.decode('utf-8')


def test_register_missing_fields(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    assert response.status_code == 400
    assert "Заполните все поля!" in response.data.decode('utf-8')


def test_register_invalid_email(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "flask.com",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    assert response.status_code == 400
    assert "Введите корректный адрес электронной почты!" in response.data.decode('utf-8')


def test_register_existing_user(client):
    existing_email = "existing@flask.flask"
    data_base.create_user("ExistingUser", existing_email, "T7Rts2l3O99P#", 'be', date(1600, 1, 1), [])
    response = client.post("/register", json={
        "nickname": "NewUser",
        "email": existing_email,
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    # noinspection PyBroadException
    try:
        data_base.delete_user("existing@flask.flask")
    except Exception:
        pass
    print(response.data.decode('utf-8'))
    assert response.status_code == 400
    assert "Пользователь с таким email уже существует!" in response.data.decode('utf-8')


def test_register_invalid_birth_date(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "gaf@flask.flask",
        "password": "T7Rts2l3O99P#",
        "birth_date": "13-40",
        "interests": []
    })
    assert response.status_code == 400
    assert "Логическая ошибка! Такого быть не должно! Дата - не дата!" in response.data.decode('utf-8')


def test_register_interests_not_a_list(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "kjihjhi@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": "not a list"
    })
    assert response.status_code == 400
    assert "Логическая ошибка! Такого быть не должно! Список - не список!" in response.data.decode('utf-8')


def test_register_unavailable_interest(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "j8j@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": ["unknown_interest"]
    })
    assert response.status_code == 400
    # noinspection IncorrectFormatting
    assert "Логическая ошибка! Такого быть не должно!" \
           " Отсутствует контроль за интересами пользователя!" in response.data.decode('utf-8')


def test_login_success(client):
    data_base.create_user("testuser", "test@test.com", "password123", 'be', date(1600, 1, 1), [])

    response = client.post("/login", json={
        "email": "test@test.com",
        "password": "password123"
    })
    # noinspection PyBroadException
    try:
        data_base.delete_user("test@test.com")
    except Exception:
        pass
    assert response.status_code == 200
    assert "access_token" in response.data.decode('utf-8')


def test_login_failed(client):
    data_base.create_user("testuser", "test@testaaaa.com", "password123", 'be', date(1600, 1, 1), [])

    response = client.post("/login", json={
        "email": "taaest@test.com",
        "password": "password123"
    })
    # noinspection PyBroadException
    try:
        data_base.delete_user("test@testaaaa.com")
    except Exception:
        pass
    assert response.status_code == 400
    assert "Пользователя с данным email не существует!" in response.data.decode('utf-8')


def test_login_missing_password(client):
    response = client.post("/login", json={
        "email": "test@test.com",
        "password": ""
    })
    assert response.status_code == 400
    assert "Введите пароль!" in response.data.decode('utf-8')


def test_login_missing_email(client):
    response = client.post("/login", json={
        "email": "",
        "password": "123"
    })
    assert response.status_code == 400
    assert "Почта не была указана!" in response.data.decode('utf-8')
