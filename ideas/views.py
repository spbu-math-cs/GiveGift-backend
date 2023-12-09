import datetime

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from core import app
from ideas.generator import generate_ideas
from DB import data_base


@app.route('/generate_ideas', methods=["POST"])
@jwt_required(optional=True)
def index():
    interests = request.json.get("interests", "")
    price_range = request.json.get("price_range", "")
    if current_email := get_jwt_identity():
        friend_id = request.json.get("friend_id", "")
        if friend_id != "":
            try:
                friend_id = int(friend_id)
            except TypeError:
                return "Передаваемый id друга должен быть числом!", 500
            user = data_base.get_user_by_email_or_none(current_email)
            if not data_base.is_friend(user.id, friend_id):
                return "Указанный человек не является Вашим другом!", 500
            friend = data_base.get_user_by_index_or_none(friend_id)
            interests = friend.interests
    if interests == "":
        return "Интересы друга не указаны!", 500
    if price_range == "":
        return "Ценовой диапазон не указан!", 500
    if type(interests) is not list:
        return "Интересы должны быть представлены в виде списка!", 500
    if len(interests) == 0:
        return []
    if type(price_range) is not list:
        return "Ценовой диапазон должен быть списком!", 500
    if len(price_range) != 2:
        return "Ценовой диапазон может содержать лишь 2 значения!", 500
    try:
        price_range = [int(price_range[0]), int(price_range[1])]
    except ValueError:
        return "Ценовой диапазон должен быть задан числами!", 500
    if price_range[0] < 0 or price_range[1] < price_range[0]:
        return "Ценовой диапазон должен быть задан неотрицательными числами, первое не превышает второго!", 500
    return generate_ideas(interests, price_range)


@app.route('/messages', methods=["GET", "POST"])
@jwt_required()
def messages():
    if email := get_jwt_identity():
        if not data_base.get_user_by_email_or_none(email).is_token_actual:
            return "Token is not actual", 401
    user = data_base.get_user_by_email_or_none(email)
    if datetime.datetime.now() - user.last_time_seen > datetime.timedelta(days=3):
        user.last_time_seen = datetime.datetime.now()
        user.add_message("", datetime.datetime.now())
    if request.method == "GET":
        return user.get_messages, 200
    message_id = request.json.get("id", "")
    try:
        message_id = int(message_id)
    except ValueError:
        return "Вместо message_id подали не число!", 401
    if user.has_message_with_id(message_id):
        return "Нет такого сообщения!", 401
    user.delete_message_with_id(message_id)
    return "OK", 200
