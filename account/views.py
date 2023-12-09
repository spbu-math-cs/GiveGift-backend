import json
import random
import re
from datetime import timedelta, datetime, timezone

from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, \
    unset_jwt_cookies, get_jwt_identity, get_jwt, \
    jwt_required

from DB import data_base
from core import app

app.config["JWT_SECRET_KEY"] = ''.join(["0123456789"[random.randint(0, 9)] for _ in range(random.randint(8, 80))])
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app=app)


@app.route('/register', methods=["POST"])
@jwt_required(optional=True)
def register():
    nickname = request.json.get("nickname", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    birth_date = request.json.get("birth_date", "")
    about = request.json.get("about", "")
    interests = request.json.get("interests", "")
    if nickname == "" or email == "" or password == "":
        return "Заполните все поля!", 401
    if len(nickname) < 2:
        return "Слишком короткий Ник!", 401
    if not re.fullmatch("\\S+@\\S+\\.\\S+", email):
        return "Введите корректный адрес электронной почты!", 401
    if not re.fullmatch("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*(\\W|_)).{8,}$", password):
        return "Введите корректный пароль! Пароль должен содержать прописные и строчные" \
               "буквы латинского алфавита, цифры. Пароль должен состоять не менее чем из" \
               "восьми символов!", 401
    if data_base.get_user_by_email_or_none(email=email):
        return "Пользователь с таким email уже существует!", 401
    if birth_date != "":
        try:
            birth_date = datetime.strptime(birth_date, "%m-%d").date()
        except ValueError:
            return "Логическая ошибка! Такого быть не должно! Дата - не дата!", 401
    if type(interests) is not list:
        return "Логическая ошибка! Такого быть не должно! Список - не список!", 401
    for interest in interests:
        if not data_base.has_tag(interest):
            return "Логическая ошибка! Такого быть не должно! Отсутствует контроль за интересами пользователя!", 401
    add_default_preferences(interests)
    data_base.create_user(nickname=nickname, email=email, password=password, about=about, birth_date=birth_date,
                          interests=interests)
    if current_email := get_jwt_identity():
        user_or_none = data_base.get_user_by_email_or_none(current_email)
        if user_or_none.is_token_actual:
            return "OK", 200
    access_token = create_access_token(identity=email)
    data_base.get_user_by_email_or_none(email).is_token_actual = True
    return {"access_token": access_token}, 200


def add_default_preferences(interests) -> None:
    for add_preference in range(5):
        index = random.randint(0, data_base.get_count_of_tags() - 1)
        interests.append(data_base.get_tags()[index])


@app.route('/login', methods=["POST"])
@jwt_required(optional=True)
def create_token():
    if email := get_jwt_identity():
        if data_base.get_user_by_email_or_none(email).is_token_actual:
            return "Token is actual", 401
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    if email == "" or password == "" or data_base.get_user_by_email_or_none(email) == "":
        return "Пользователя с данным email не существует!", 401
    if not data_base.has_user(email, password):
        return "Неверные имя пользователя или пароль!", 401
    access_token = create_access_token(identity=email)
    data_base.get_user_by_email_or_none(email).is_token_actual = True
    return {"access_token": access_token}, 200


def set_info():
    user_id = request.json.get("id", "")
    nickname = request.json.get("nickname", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    birth_date = request.json.get("birth_date", "")
    about = request.json.get("about", "")
    interests = request.json.get("interests", "")
    if email == "" or not re.fullmatch("\\S+@\\S+\\.\\S+", email):
        return "Заполните поле email!", 401
    if password == "" or not re.fullmatch("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*(\\W|_)).{8,}$", password):
        return "Введите корректный пароль!", 401
    if user_id == "":
        return "Введённый id пуст!", 401
    if data_base.get_user_by_index_or_none(user_id) is None:
        return "Нет пользователя с данным id!", 401
    if data_base.get_user_by_email_or_none(email) is not None:
        return "Пользователь с данным email уже существует!", 401
    if birth_date != "":
        try:
            birth_date = datetime.strptime(birth_date, "%m-%d").date()
        except ValueError:
            return "Логическая ошибка! Дата не парсится!", 401
    if type(interests) is not list:
        return "Логическая ошибка! Список не парсится!", 401
    for interest in interests:
        if not data_base.has_tag(interest):
            return "К сожалению, выбранный тег не поддерживается!", 401
    data_base.set_to_user_with_id(user_id=int(user_id), email=email, about=about, interests=interests,
                                  nickname=nickname, birth_date=birth_date, password=password)
    return "OK", 200


def get_safe_user_info(user) -> dict:
    return {
        "id": str(user.id),
        "nickname": str(user.nickname),
        "email": str(user.email),
        "about": str(user.about),
        "birth_date": str(user.birth_date),
        "interests": str(user.interests)
    }


def get_user_info_by_id(user_id: int):
    user = data_base.get_user_by_index_or_none(user_id)
    if user is None:
        raise IndexError("Unsupported None value return!")
    return get_safe_user_info(user)


@app.route('/account', methods=["GET", "POST"])
@jwt_required()
def get_account_info():
    if email := get_jwt_identity():
        if not data_base.get_user_by_email_or_none(email).is_token_actual:
            return "Token is not actual", 401
    if request.method == 'POST':
        return set_info()
    user = data_base.get_user_by_email_or_none(email)
    return get_safe_user_info(user), 200


@app.route('/get_user_info/<i>', methods=["GET"])
@jwt_required(optional=True)
def get_user_info(i):
    email = get_jwt_identity()
    try:
        i = int(i)
    except ValueError:
        return 404
    if email is not None and i == -1:
        if not data_base.get_user_by_email_or_none(email).is_token_actual:
            return "Token is not actual", 401
        user = data_base.get_user_by_email_or_none(email)
        return get_safe_user_info(user), 200
    if questioned_user := data_base.get_user_by_index_or_none(i):
        return get_safe_user_info(questioned_user), 200
    if i == -1:
        return "Зарегистрируйтесь или войдите!", 500
    return "Не существует человека с таким id!", 500


@app.route('/friends', methods=["GET", "DELETE"])
@jwt_required()
def friends():
    if email := get_jwt_identity():
        if not data_base.get_user_by_email_or_none(email).is_token_actual:
            return "Token is not actual", 401
    user = data_base.get_user_by_email_or_none(email)
    if request.method == "GET":
        return {
            "friends": list(map(lambda user_id: get_user_info_by_id(user_id), data_base.get_friends(user.id))),
            "incoming_requests": list(map(lambda user_id: get_user_info_by_id(user_id),
                                          data_base.get_incoming_requests(user.id))),
            "outgoing_requests": list(map(lambda user_id: get_user_info_by_id(user_id),
                                          data_base.get_outgoing_requests(user.id)))
        }, 200
    friend_id = request.json.get("friend_id", "")
    try:
        friend_id = int(friend_id)
    except ValueError:
        return "Вместо friend_id подали не число!", 401
    if data_base.get_user_by_index_or_none(friend_id) is None:
        return "Упомянутый друг не найден в базе!", 401
    if not data_base.is_friend(user.id, friend_id):
        return "Эти люди - не друзья!", 401

    if request.method == "DELETE":
        data_base.remove_friend(user.id, friend_id)
        return "OK", 200
    return "Something went wrong", 404


@app.route('/outgoing_friend_request', methods=["DELETE", "POST"])
@jwt_required()
def outgoing_friend_request():
    if email := get_jwt_identity():
        if not data_base.get_user_by_email_or_none(email).is_token_actual:
            return "Token is not actual", 401
    user = data_base.get_user_by_email_or_none(email)
    friend_id = request.json.get("friend_id", "")
    try:
        friend_id = int(friend_id)
    except ValueError:
        return "Вместо friend_id подали не число!", 401
    if data_base.get_user_by_index_or_none(friend_id) is None:
        return "Упомянутый друг не найден в базе!", 401
    if request.method == "POST":
        if data_base.has_outgoing_requests(user.id, friend_id):
            return "Уже есть исходящий запрос к этому другу!", 401
        data_base.send_friend_request(user.id, friend_id)
        return "OK", 200
    if not data_base.has_outgoing_requests(user.id, friend_id):
        return "Не было исходящего запроса к этому другу!", 401
    if request.method == "DELETE":
        data_base.remove_friend_request(user.id, friend_id)
        return "OK", 200
    return "Something went wrong", 404


@app.route('/incoming_friend_request', methods=["DELETE", "POST"])
@jwt_required()
def incoming_friend_request():
    if email := get_jwt_identity():
        if not data_base.get_user_by_email_or_none(email).is_token_actual:
            return "Token is not actual", 401
    user = data_base.get_user_by_email_or_none(email)
    friend_id = request.json.get("friend_id", "")
    try:
        friend_id = int(friend_id)
    except ValueError:
        return "Вместо friend_id подали не число!", 401
    if data_base.get_user_by_index_or_none(friend_id) is None:
        return "Упомянутый друг не найден в базе!", 401
    if not data_base.has_incoming_requests(user.id, friend_id):
        return "Нет входящего запроса от упомянутого друга", 401
    if request.method == "DELETE":
        data_base.remove_friend_request(friend_id, user.id)
        return "OK", 200
    if request.method == "POST":
        data_base.accept_friend_request(friend_id, user.id)
        return "OK", 200
    return "Something went wrong", 404


@app.route('/logout', methods=["POST"])
@jwt_required()
def logout():
    if email := get_jwt_identity():
        if not data_base.get_user_by_email_or_none(email).is_token_actual:
            return "Token is not actual", 401
    response = jsonify({"message": "logout successful", "code": 200})
    unset_jwt_cookies(response)
    data_base.get_user_by_email_or_none(email).is_token_actual = False
    return response


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data['access_token'] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response
