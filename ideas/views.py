import datetime
import random

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
                return "Передаваемый id друга должен быть числом!", 400
            user = data_base.get_user_by_email_or_none(current_email)
            if not data_base.is_friend(user.id, friend_id):
                return "Указанный человек не является Вашим другом!", 400
            friend = data_base.get_user_by_index_or_none(friend_id)
            interests = data_base.get_user_tags(friend.id)
    if interests == "":
        return "Интересы друга не указаны!", 400
    if price_range == "":
        return "Ценовой диапазон не указан!", 400
    if type(interests) is not list:
        return "Интересы должны быть представлены в виде списка!", 400
    if len(interests) == 0:
        return []
    if type(price_range) is not list:
        return "Ценовой диапазон должен быть списком!", 400
    if len(price_range) != 2:
        return "Ценовой диапазон может содержать лишь 2 значения!", 400
    try:
        price_range = [int(price_range[0]), int(price_range[1])]
    except ValueError:
        return "Ценовой диапазон должен быть задан числами!", 400
    if price_range[0] < 0 or price_range[1] < price_range[0]:
        return "Ценовой диапазон должен быть задан неотрицательными числами, первое не превышает второго!", 400
    return generate_ideas(interests, price_range)


@app.route('/__messages', methods=["GET", "POST"])
@jwt_required()
def messages():
    if email := get_jwt_identity():
        if not data_base.get_user_by_email_or_none(email).is_token_actual:
            return "Token is not actual", 401

    user = data_base.get_user_by_email_or_none(email)
    if datetime.datetime.now() - user.last_time_seen > datetime.timedelta(days=3):
        requested_users = data_base.get_friends(user.id)
        if len(requested_users) > 0:
            user.last_time_seen = datetime.datetime.now()
            requested_user_id = requested_users[random.randint(0, len(requested_users) - 1)]
            requested_user = data_base.get_user_by_index_or_none(requested_user_id)
            ideas = []
            while len(ideas) == 0:
                ideas = generate_ideas(requested_user.get_interests, [0, 1000])
            data_base.add_message(
                user.id,
                f"Подари {requested_user.nickname} {ideas[0]['title']}",
                datetime.datetime.now()
            )
    if request.method == "GET":
        return data_base.get_messages(user.id), 200
    message_id = request.json.get("id", "")
    try:
        message_id = int(message_id)
    except ValueError:
        return "Вместо message_id подали не число!", 400
    if data_base.has_message_with_id(user.id, message_id):
        return "Нет такого сообщения!", 400
    data_base.delete_message_with_id(user.id, message_id)
    return "OK", 200
