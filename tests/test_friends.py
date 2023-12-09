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


def add_users_to_db(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "flask@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    if response.status_code == 200:
        token1 = response.json['access_token']
    elif response.text == "Пользователь с таким email уже существует!":
        response = client.post("/register", json={
            "email": "flask@flask.flask",
            "password": "T7Rts2l3O99P#",
        })
        assert response.status_code == 200
        token1 = response.json['access_token']
    else:
        assert False
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "flask2@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    if response.status_code == 200:
        token2 = response.json['access_token']
    elif response.text == "Пользователь с таким email уже существует!":
        response = client.post("/register", json={
            "email": "flask2@flask.flask",
            "password": "T7Rts2l3O99P#",
        })
        assert response.status_code == 200
        token2 = response.json['access_token']
    else:
        assert False
    response = client.get("/account",
                          headers={"Authorization": "Bearer {}".format(token1)})
    assert response.status_code == 200
    user1_id = response.json["id"]
    response = client.get("/account",
                          headers={"Authorization": "Bearer {}".format(token2)})
    assert response.status_code == 200
    user2_id = response.json["id"]
    return token1, user1_id, token2, user2_id


def return_two_friends(client):
    token1, user1_id, token2, user2_id = send_outgoing_request(client)
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token2)})
    assert response.status_code == 200
    assert len(response.json["__friends"]) == 0
    assert len(response.json["__incoming_requests"]) == 1
    assert len(response.json["__outgoing_requests"]) == 0
    assert response.json["__incoming_requests"][0]["id"] == user1_id
    response = client.post("/incoming_friend_request",
                           headers={"Authorization": "Bearer {}".format(token2)},
                           json={
                               "friend_id": user1_id
                           }
                           )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token2)})
    assert response.status_code == 200
    assert len(response.json["__friends"]) == 1
    assert len(response.json["__incoming_requests"]) == 0
    assert len(response.json["__outgoing_requests"]) == 0
    assert response.json["__friends"][0]["id"] == user1_id
    return token1, user1_id, token2, user2_id


@pytest.mark.order(0)
def test_add_friends(client):
    return_two_friends(client)


@pytest.mark.order(1)
def test_remove_friend(client):
    token1, user1_id, token2, user2_id = return_two_friends(client)
    response = client.delete("/friend",
                             headers={"Authorization": "Bearer {}".format(token2)},
                             json={
                                 "friend_id": user1_id
                             }
                             )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token2)})
    assert response.status_code == 200
    assert len(response.json["__friends"]) == 0
    assert len(response.json["__incoming_requests"]) == 0
    assert len(response.json["__outgoing_requests"]) == 0
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token1)})
    assert response.status_code == 200
    assert len(response.json["__friends"]) == 0
    assert len(response.json["__incoming_requests"]) == 0
    assert len(response.json["__outgoing_requests"]) == 0


@pytest.mark.order(2)
def test_remove_friend_request(client):
    token1, _, token2, user2_id = send_outgoing_request(client)
    response = client.delete("/outgoing_friend_request",
                             headers={"Authorization": "Bearer {}".format(token1)},
                             json={
                                 "friend_id": user2_id
                             }
                             )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token1)})
    assert response.status_code == 200
    assert len(response.json["__friends"]) == 0
    assert len(response.json["__incoming_requests"]) == 0
    assert len(response.json["__outgoing_requests"]) == 0
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token2)})
    assert response.status_code == 200
    assert len(response.json["__friends"]) == 0
    assert len(response.json["__incoming_requests"]) == 0
    assert len(response.json["__outgoing_requests"]) == 0


def send_outgoing_request(client):
    token1, user1_id, token2, user2_id = add_users_to_db(client)
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token1)})
    assert response.status_code == 200
    assert len(response.json["__friends"]) == 0
    assert len(response.json["__incoming_requests"]) == 0
    assert len(response.json["__outgoing_requests"]) == 0
    response = client.post("/outgoing_friend_request",
                           headers={"Authorization": "Bearer {}".format(token1)},
                           json={
                               "friend_id": user2_id
                           }
                           )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token1)})
    assert response.status_code == 200
    assert len(response.json["__friends"]) == 0
    assert len(response.json["__incoming_requests"]) == 0
    assert len(response.json["__outgoing_requests"]) == 1
    assert response.json["__outgoing_requests"][0]["id"] == user2_id
    return token1, user1_id, token2, user2_id
