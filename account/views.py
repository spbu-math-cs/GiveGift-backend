import base64
from json import dumps
from os import path, remove
from random import randint, sample
from re import fullmatch
from datetime import timedelta, datetime, timezone
from dateutil import parser
from flask import request, jsonify
# noinspection IncorrectFormatting
from flask_jwt_extended import JWTManager, create_access_token, unset_jwt_cookies,\
    get_jwt_identity, get_jwt, jwt_required

from DB import data_base
from core import app

app.config["JWT_SECRET_KEY"] = ''.join(["0123456789"[randint(0, 9)] for _ in range(randint(8, 80))])
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1) для теста обновления токена
app.config["UPLOAD_FOLDER"] = "images"
app.config["MAX_CONTENT_LENGTH"] = 640 * 480
EXTENSIONS = ['png', 'bmp', 'jpg']


def is_name_allowed(filename: str) -> bool:
    print(filename.rsplit('.', 1)[1].lower())
    # noinspection IncorrectFormatting
    return '.' in filename and '/' not in filename and '\\' not in filename and \
           filename.rsplit('.', 1)[1].lower() in EXTENSIONS


jwt = JWTManager(app=app)


# noinspection IncorrectFormatting
@app.route('/register', methods=["POST"])
@jwt_required(optional=True)
def register():
    nickname = request.json.get("nickname", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    birth_date = request.json.get("birth_date", "")
    about = request.json.get("about", "")
    interests = request.json.get("interests", "")
    avatar = request.json.get("avatar", "")
    if nickname == "" or email == "" or password == "":
        return "Заполните все поля!", 400
    if len(nickname) < 2:
        return "Слишком короткий Ник!", 400
    if not fullmatch("\\S+@\\S+\\.\\S+", email):
        return "Введите корректный адрес электронной почты!", 400
    if not fullmatch("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*(\\W|_)).{8,}$", password):
        return "Введите корректный пароль! Пароль должен содержать прописные и строчные"\
               "буквы латинского алфавита, цифры. Пароль должен состоять не менее чем из"\
               "восьми символов!", 400
    if data_base.get_user_by_email_or_none(email=email):
        return "Пользователь с таким email уже существует!", 400
    if birth_date != "":
        try:
            birth_date = datetime.strptime(birth_date, "%d-%m-%Y").date()
        except ValueError:
            return "Логическая ошибка! Такого быть не должно! Дата - не дата!", 400
    else:
        birth_date = None
    if type(interests) is not list:
        return "Логическая ошибка! Такого быть не должно! Список - не список!", 400
    for interest in interests:
        if not data_base.has_tag(interest):
            return "Логическая ошибка! Такого быть не должно! Отсутствует контроль за интересами пользователя!", 400
    interests = get_random_preferences(5)
    data_base.create_user(nickname=nickname, email=email, password=password, about=about, birth_date=birth_date,
                          interests=interests)
    user_id = data_base.get_user_by_email_or_none(email).id
    set_avatar(avatar=avatar, user_id=user_id)
    if current_email := get_jwt_identity():
        user_or_none = data_base.get_user_by_email_or_none(current_email)
        if user_or_none.is_token_actual:
            return "OK", 200
    access_token = create_access_token(identity=email)
    data_base.set_user_token_as(user_id, True)
    return {"access_token": access_token}, 200


def get_random_preferences(num_of_preferences) -> [str]:
    if num_of_preferences < data_base.get_count_of_tags():
        return sample(data_base.get_tags(), num_of_preferences)
    return []


@app.route('/login', methods=["POST"])
@jwt_required(optional=True)
def create_token():
    if email := get_jwt_identity():
        if data_base.get_user_by_email_or_none(email).is_token_actual:
            return "Token is actual", 401
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    if email == "":
        return "Почта не была указана!", 400
    if password == "":
        return "Введите пароль!", 400
    if data_base.get_user_by_email_or_none(email) is None:
        return "Пользователя с данным email не существует!", 400
    if not data_base.has_user(email, password):
        return "Неверные имя пользователя или пароль!", 400
    access_token = create_access_token(identity=email)
    data_base.set_user_token_as(data_base.get_user_by_email_or_none(email).id, True)
    return {"access_token": access_token}, 200


def set_info():
    user_id = request.json.get("id", "")
    nickname = request.json.get("nickname", "")
    email = request.json.get("email", "")
    birth_date = request.json.get("birth_date", "")
    about = request.json.get("about", "")
    interests = request.json.get("interests", "")
    avatar = request.json.get("avatar", "")
    if email == "" or not fullmatch("\\S+@\\S+\\.\\S+", email):
        return "Заполните поле email!", 400
    if user_id == "":
        return "Введённый id пуст!", 400
    if data_base.get_user_by_index_or_none(user_id) is None:
        return "Нет пользователя с данным id!", 400
    if birth_date != "" and birth_date is not None:
        try:
            birth_date = parser.parse(birth_date).date()
        except ValueError:
            return "Логическая ошибка! Дата не парсится!", 400
    if type(interests) is not list:
        return "Логическая ошибка! Список не парсится!", 400
    for interest in interests:
        if not data_base.has_tag(interest):
            return "К сожалению, выбранный тег не поддерживается!", 400
    try:
        user_id = int(user_id)
    except ValueError:
        return "Вместо id подали не число!"
    set_avatar(avatar, user_id)
    data_base.set_to_user_with_id(user_id=user_id, email=email, about=about, interests=interests,
                                  nickname=nickname, birth_date=birth_date)
    return "OK", 200


def set_avatar(avatar, user_id):
    if avatar == "":
        file_path = path.join(app.config['UPLOAD_FOLDER'], str(user_id) + ".jpg")
        if path.exists(file_path):
            remove(file_path)
    else:
        binary_image = base64.decodebytes(bytes(avatar, 'utf-8'))
        with open(path.join(app.config['UPLOAD_FOLDER'], str(user_id) + ".jpg"), "wb") as file:
            file.write(binary_image)


def get_safe_user_info_simple(user) -> dict:
    avatar = ""
    file_path = path.join(app.config['UPLOAD_FOLDER'], str(user.id) + ".jpg")
    if path.exists(file_path):
        with open(path.join(app.config['UPLOAD_FOLDER'], str(user.id) + ".jpg"), "rb") as file:
            binary_image: bytes = file.read()
            avatar: str = base64.encodebytes(binary_image).decode('utf-8')
    return {
        "id": str(user.id),
        "nickname": str(user.nickname),
        "email": str(user.email),
        "about": str(user.about),
        "birth_date": user.birth_date,  # strftime("%d-%m-%Y")
        "interests": data_base.get_user_tags(user.id),
        "is_admin": str(user.is_admin),
        "avatar": avatar
    }


def get_safe_user_info(user) -> dict:
    data: dict = get_safe_user_info_simple(user)
    data["friends"] = [
        get_safe_user_info_simple(data_base.get_user_by_index_or_none(friend_id))
        for friend_id in data_base.get_friends(user.id)
    ]
    return data


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
    if email is not None and i == 0:
        user = data_base.get_user_by_email_or_none(email)
        if not user.is_token_actual:
            return "Token is not actual", 401
        user_info = get_safe_user_info(user)
        user_info["is_me"] = True
        return user_info, 200
    if questioned_user := data_base.get_user_by_index_or_none(i):
        user_info = get_safe_user_info(questioned_user)
        user_info["is_me"] = False
        if email is not None:
            if not data_base.get_user_by_email_or_none(email).is_token_actual:
                return "Token is not actual", 401
            user = data_base.get_user_by_email_or_none(email)
            user_info["is_me"] = (user.id == questioned_user.id)
        return user_info, 200
    if i == 0:
        return "Зарегистрируйтесь или войдите!", 400
    return "Не существует человека с таким id!", 400


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
        return "Вместо friend_id подали не число!", 400
    if data_base.get_user_by_index_or_none(friend_id) is None:
        return "Упомянутый друг не найден в базе!", 404
    if not data_base.is_friend(user.id, friend_id):
        return "Эти люди - не друзья!", 400

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
        return "Вместо friend_id подали не число!", 400
    if data_base.get_user_by_index_or_none(friend_id) is None:
        return "Упомянутый друг не найден в базе!", 404
    if request.method == "POST":
        if user.id == friend_id:
            return "Невозможно добавить в друзья самого себя!", 400
        if data_base.has_outgoing_request(user.id, friend_id):
            return "Уже есть исходящий запрос к этому другу!", 400
        if data_base.has_incoming_request(user.id, friend_id):
            data_base.accept_friend_request(friend_id, user.id)
        data_base.send_friend_request(user.id, friend_id)
        return "OK", 200
    if not data_base.has_outgoing_request(user.id, friend_id):
        return "Не было исходящего запроса к этому другу!", 400
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
        return "Вместо friend_id подали не число!", 400
    if data_base.get_user_by_index_or_none(friend_id) is None:
        return "Упомянутый друг не найден в базе!", 404
    if not data_base.has_incoming_request(user.id, friend_id):
        return "Нет входящего запроса от упомянутого друга", 400
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
    response = jsonify({"msg": "logout successful", "code": 200})
    unset_jwt_cookies(response)
    data_base.set_user_token_as(data_base.get_user_by_email_or_none(email).id, False)
    return response


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30, seconds=30))
        # target_timestamp = datetime.timestamp(now + timedelta(seconds=30)) для теста обновления токена
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data['access_token'] = access_token
                response.data = dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response
