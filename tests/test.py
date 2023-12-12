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


def test_request_example(client):
    # response = client.get("/posts")
    assert True  # b"<h2>Hello, World!</h2>" in response.data


def test_register_user(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "a@flask.flask",
        "password": "T7Rts2l3O99P#",
        "_interests": []
    })
    token = response.json['access_token']
    assert response.status_code == 200

def test_register_user_short_nick(client):
    response = client.post("/register", json={
        "nickname": "g",
        "email": "flask@flask.flask",
        "password": "T7Rts2l3O99P#",
        "_interests": []
    })
    assert response.status_code == 401
    assert "Слишком короткий Ник!" in response.data.decode('utf-8')

def test_register_missing_fields(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "password": "T7Rts2l3O99P#",
        "_interests": []
    })
    assert response.status_code == 401
    assert "Заполните все поля!" in response.data.decode('utf-8')

def test_register_invalid_email(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "flask.com",
        "password": "T7Rts2l3O99P#",
        "_interests": []
    })
    assert response.status_code == 401
    assert "Введите корректный адрес электронной почты!" in response.data.decode('utf-8')

def test_register_existing_user(client):
    existing_email = "existing@flask.flask"
    data_base.create_user("ExistingUser", existing_email, "T7Rts2l3O99P#", 'be', date(1600, 1, 1), [])
    response = client.post("/register", json={
        "nickname": "NewUser",
        "email": existing_email,
        "password": "T7Rts2l3O99P#",
        "_interests": []
    })
    assert response.status_code == 401
    assert "Пользователь с таким email уже существует!" in response.data.decode('utf-8')

def test_register_invalid_birth_date(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "gaf@flask.flask",
        "password": "T7Rts2l3O99P#",
        "birth_date": "13-40",
        "_interests": []
    })
    assert response.status_code == 401
    assert "Логическая ошибка! Такого быть не должно! Дата - не дата!" in response.data.decode('utf-8')

def test_register_interests_not_a_list(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "kjihjhi@flask.flask",
        "password": "T7Rts2l3O99P#",
        "_interests": "not a list"
    })
    assert response.status_code == 401
    assert "Логическая ошибка! Такого быть не должно! Список - не список!" in response.data.decode('utf-8')

def test_register_unavailable_interest(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "j8j@flask.flask",
        "password": "T7Rts2l3O99P#",
        "_interests": ["unknown_interest"]
    })
    assert response.status_code == 401
    assert "Логическая ошибка! Такого быть не должно! Отсутствует контроль за интересами пользователя!" in response.data.decode('utf-8')


def test_login_success(client):
    # Добавьте пользователя в базу данных
    data_base.create_user("testuser", "test@test.com", "password123", 'be', date(1600, 1, 1), [])

    response = client.post("/login", json={
        "email": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.data.decode('utf-8')

def test_login_failed(client):
    # Добавьте пользователя в базу данных
    data_base.create_user("testuser", "test@testaaaa.com", "password123", 'be', date(1600, 1, 1), [])

    response = client.post("/login", json={
        "email": "taaest@test.com",
        "password": "password123"
    })
    assert response.status_code == 401
    assert "Неверные имя пользователя или пароль!" in response.data.decode('utf-8')

def test_login_missing_password(client):
    response = client.post("/login", json={
        "email": "test@test.com",
        "password": ""
    })
    assert response.status_code == 401
    assert "Введите пароль!" in response.data.decode('utf-8')

def test_login_missing_email(client):
    response = client.post("/login", json={
        "email": "",
        "password": "123"
    })
    assert response.status_code == 401
    assert "Почта не была указана!" in response.data.decode('utf-8')
