import json
import random
from datetime import timedelta, datetime, timezone, date
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, \
    unset_jwt_cookies, get_jwt_identity, get_jwt, \
    jwt_required
from DB import data_base

from core import app

app.config["JWT_SECRET_KEY"] = "123456"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)


@app.route('/register', methods=["POST"])
def register():
    nickname = request.json.get("nickname", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    birth_date = request.json.get("birth_date", None)
    about = request.json.get("about", None)
    interests = request.json.get("interests", None)
    if email is None or password is None or data_base.has_user_as(email, password):
        return {"response": "500", "message": "401"}
    if birth_date is not None:
        try:
            birth_date = datetime.strptime(birth_date, "%m-%d").date()
        except ValueError:
            return {"response": "500", "message": "401"}
    if type(interests) is not list:
        return {"response": "500", "message": "401"}
    for interest in interests:
        if not data_base.has_tag_as(interest):
            return {"response": "500", "message": "401"}
    for add_preference in range(5):
        index = random.randint(0, data_base.get_tag_count())
        interests.append(data_base.get_tags()[index])
    data_base.create_user(nickname, email, password, about, birth_date, interests)
    # TODO to log in
    return {"response": "200", "message": "OK"}


@app.route('/login', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email is None or password is None or not data_base.has_user_as(email, password):
        return {"response": "500", "message": "401"}
    access_token = create_access_token(identity=email)
    return {"response": "200", "message": "OK", "access_token": access_token}


@app.route('/account', methods=["GET", "POST"])
@jwt_required()
def get_account_info():  # TODO refactor
    if request.method == 'POST':
        user_id = request.json.get("id", None)
        nickname = request.json.get("nickname", None)
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        birth_date = request.json.get("birth_date", None)
        about = request.json.get("about", None)
        interests = request.json.get("interests", None)
        if email is None or password is None or \
                user_id is None or \
                not data_base.has_user_with_id(user_id) or data_base.get_user_by_name(email) is not None:
            return {"response": "500", "message": "401"}
        if birth_date is not None:
            try:
                birth_date = datetime.strptime(birth_date, "%m-%d").date()
            except ValueError:
                return {"response": "500", "message": "401"}
        if type(interests) is not list:
            return {"response": "500", "message": "401"}
        for interest in interests:
            if not data_base.has_tag_as(interest):
                return {"response": "500", "message": "401"}
        for add_preference in range(5):
            index = random.randint(0, data_base.get_tag_count())
            interests.append(data_base.get_tags()[index])
        user = data_base.get_user_with_id(int(user_id))
        user.about = about
        user.email = email
        user.interests = interests
        user.nickname = nickname
        user.birth_date = birth_date
        user.password_hash(password)
        return {"response": "200", "message": "OK"}
    user_name: str = get_jwt_identity()
    user = data_base.get_user_by_name(user_name)
    if user is None:
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
    response = jsonify({"response": "200", "message": "logout successful"})
    unset_jwt_cookies(response)
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
