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


@pytest.fixture()
def return_two_users(my_app):
    response = my_app.post("/register", json={
        "nickname": "Flask",
        "email": "flask@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    assert response.status_code == 200
    token = response.json['access_token']
    response = my_app.post("/register", json={
        "nickname": "Flask2",
        "email": "flask2@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    assert response.status_code == 200
    return my_app.test_client()


def test_add_friends(return_two_users):
    # response = client.post("/register", json={
    #     "nickname": "Flask",
    #     "email": "flask@flask.flask",
    #     "password": "T7Rts2l3O99P#",
    #     "interests": []
    # })
    # assert response.status_code == 200
    # token = response.json['access_token']
    # response = client.post("/register", json={
    #     "nickname": "Flask2",
    #     "email": "flask2@flask.flask",
    #     "password": "T7Rts2l3O99P#",
    #     "interests": []
    # })
    # assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 0
    response = client.post("/outgoing_friend_request",
                           headers={"Authorization": "Bearer {}".format(token)},
                           json={
                               "friend_id": "3"
                           }
                           )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 1
    assert response.json["outgoing_requests"][0]["id"] == '3'
    response = client.post("/logout",
                           headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    response = client.post("/login", json={
        "email": "flask2@flask.flask",
        "password": "T7Rts2l3O99P#",
    })
    assert response.status_code == 200
    token = response.json["access_token"]
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 1
    assert len(response.json["outgoing_requests"]) == 0
    assert response.json["incoming_requests"][0]["id"] == '2'
    response = client.post("/incoming_friend_request",
                           headers={"Authorization": "Bearer {}".format(token)},
                           json={
                               "friend_id": "2"
                           }
                           )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 1
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 0
    assert response.json["friends"][0]["id"] == '2'


def test_remove_friend(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "flask@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    assert response.status_code == 200
    token = response.json['access_token']
    response = client.post("/register", json={
        "nickname": "Flask2",
        "email": "flask2@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 0
    response = client.post("/outgoing_friend_request",
                           headers={"Authorization": "Bearer {}".format(token)},
                           json={
                               "friend_id": "3"
                           }
                           )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 1
    assert response.json["outgoing_requests"][0]["id"] == '3'
    response = client.post("/logout",
                           headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    response = client.post("/login", json={
        "email": "flask2@flask.flask",
        "password": "T7Rts2l3O99P#",
    })
    assert response.status_code == 200
    token = response.json["access_token"]
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 1
    assert len(response.json["outgoing_requests"]) == 0
    assert response.json["incoming_requests"][0]["id"] == '2'
    response = client.post("/incoming_friend_request",
                           headers={"Authorization": "Bearer {}".format(token)},
                           json={
                               "friend_id": "2"
                           }
                           )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 1
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 0
    response = client.delete("/friend",
                             headers={"Authorization": "Bearer {}".format(token)},
                             json={
                                 "friend_id": "2"
                             }
                             )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 0
    response = client.post("/logout",
                           headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    response = client.post("/login", json={
        "email": "flask@flask.flask",
        "password": "T7Rts2l3O99P#",
    })
    assert response.status_code == 200
    token = response.json["access_token"]
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 0


def test_remove_friend_request(client):
    response = client.post("/register", json={
        "nickname": "Flask",
        "email": "flask@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    assert response.status_code == 200
    token = response.json['access_token']
    response = client.post("/register", json={
        "nickname": "Flask2",
        "email": "flask2@flask.flask",
        "password": "T7Rts2l3O99P#",
        "interests": []
    })
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 0
    response = client.post("/outgoing_friend_request",
                           headers={"Authorization": "Bearer {}".format(token)},
                           json={
                               "friend_id": "3"
                           }
                           )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 1
    assert response.json["outgoing_requests"][0]["id"] == '3'
    response = client.delete("/outgoing_friend_request",
                             headers={"Authorization": "Bearer {}".format(token)},
                             json={
                                 "friend_id": "3"
                             }
                             )
    assert response.status_code == 200
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 0
    response = client.post("/logout",
                           headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    response = client.post("/login", json={
        "email": "flask2@flask.flask",
        "password": "T7Rts2l3O99P#",
    })
    assert response.status_code == 200
    token = response.json["access_token"]
    response = client.get("/friend",
                          headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 200
    assert len(response.json["friends"]) == 0
    assert len(response.json["incoming_requests"]) == 0
    assert len(response.json["outgoing_requests"]) == 0
