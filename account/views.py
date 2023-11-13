import json
import random
from datetime import timedelta, datetime, timezone
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, \
    unset_jwt_cookies, get_jwt_identity, get_jwt, \
    jwt_required
from DB import data_base

from core import app

app.config["JWT_SECRET_KEY"] = "123456"
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
    if email == "" or password == "" or data_base.get_user_by_name_or_none(email=email) != "":
        return {"response": "500", "message": "Пользователь с таким email уже существует. Введите другой email!"}
    if birth_date != "":
        try:
            birth_date = datetime.strptime(birth_date, "%m-%d").date()
        except ValueError:
            return {"response": "500", "message": "Логическая ошибка! Такого быть не должно! Дата - не дата!"}
    if type(interests) is not list:
        return {"response": "500", "message": "Логическая ошибка! Такого быть не должно! Список - не список!"}
    for interest in interests:
        if not data_base.has_tag(interest):
            return {"response": "500", "message": "Логическая ошибка! Такого быть не должно! Отсутствует контроль за интересами пользователя!"}
    add_default_preferences(interests)
    data_base.create_user(nickname=nickname, email=email, password=password, about=about, birth_date=birth_date, interests=interests)
    if email := get_jwt_identity():
        if data_base.get_user_by_name_or_none(email).is_token_actual:
            return {"response": "200", "message": "OK"}  # TODO was loged in
    access_token = create_access_token(identity=email)
    data_base.get_user_by_name_or_none(email).is_token_actual = True
    return {"response": "200", "message": "OK", "access_token": access_token}


def add_default_preferences(interests) -> None:
    for add_preference in range(5):
        index = random.randint(0, data_base.get_tags_count() - 1)
        interests.append(data_base.get_tags()[index])


@app.route('/login', methods=["POST"])
@jwt_required(optional=True)
def create_token():
    if email := get_jwt_identity():
        if data_base.get_user_by_name_or_none(email).is_token_actual:
            return {"response": "500", "message": "Token is actual"}
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    if email == "" or password == "" or data_base.get_user_by_name_or_none(email) == "":
        return {"response": "500", "message": "Пользователя с данным email не существует!"}
    if not data_base.has_user(email, password):
        return {"response": "500", "message": "Неверные имя пользователя или пароль!"}
    access_token = create_access_token(identity=email)
    data_base.get_user_by_name_or_none(email).is_token_actual = True
    return {"response": "200", "message": "OK", "access_token": access_token}


def set_info() -> dict:
    user_id = request.json.get("id", "")
    nickname = request.json.get("nickname", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    birth_date = request.json.get("birth_date", "")
    about = request.json.get("about", "")
    interests = request.json.get("interests", "")
    if email == "" or password == "" or \
            user_id == "" or \
            not data_base.has_user_with_id(user_id) or data_base.get_user_by_name_or_none(email) != "":
        return {"response": "500", "message": "401"}
    if birth_date != "":
        try:
            birth_date = datetime.strptime(birth_date, "%m-%d").date()
        except ValueError:
            return {"response": "500", "message": "401"}
    if type(interests) is not list:
        return {"response": "500", "message": "401"}
    for interest in interests:
        if not data_base.has_tag(interest):
            return {"response": "500", "message": "401"}
    data_base.set_to_user_with_id(user_id=int(user_id), email=email, about=about, interests=interests, nickname=nickname, birth_date=birth_date, password=password)
    return {"response": "200", "message": "OK"}


@app.route('/account', methods=["GET", "POST"])
@jwt_required()
def get_account_info():
    if email := get_jwt_identity():
        if not data_base.get_user_by_name_or_none(email).is_token_actual:
            return {"response": "500", "message": "Token is not actual"}
    if request.method == 'POST':
        return set_info()
    email: str = get_jwt_identity()
    user = data_base.get_user_by_name_or_none(email)
    if user == "":
        return {"response": "500", "message": "401"}
    return {
        "id": str(user.id),
        "nickname": user.nickname,
        "email": user.email,
        "about": user.about,
        "birth_date": str(user.birth_date),
        "interests": user.interests
    }


@app.route('/logout', methods=["POST"])
@jwt_required()
def logout():
    if email := get_jwt_identity():
        if not data_base.get_user_by_name_or_none(email).is_token_actual:
            return {"response": "500", "message": "Token is not actual"}
    response = jsonify({"response": "200", "message": "logout successful"})
    unset_jwt_cookies(response)
    data_base.get_user_by_name_or_none(email).is_token_actual = False
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
