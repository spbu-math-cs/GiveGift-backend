from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from core import app
from ideas.generator import generate_ideas
from DB import data_base


@app.route('/generate_ideas', methods=["POST"])
@jwt_required(optional=True)
def index():
    interests = request.json.get("interests", "")
    num_of_ideas = request.json.get("num_of_ideas", "")
    price_range = request.json.get("price_range", "")
    if current_email := get_jwt_identity():
        friend_id = request.json.get("friend_id", "")
        if friend_id != "":
            try:
                friend_id = int(friend_id)
            except TypeError:
                return "4011", 500
            user = data_base.get_user_by_email_or_none(current_email)
            if not data_base.is_friend(user.id, friend_id):
                return "4011", 500
            friend = data_base.get_user_by_index_or_none(friend_id)
            interests = friend.interests
    if interests == "" or num_of_ideas == "" or price_range == "":
        return "Не все значения указаны!", 500
    if type(interests) is not list:
        return "Интересы должны быть представлены в виде списка!", 500
    try:
        num_of_ideas = int(num_of_ideas)
    except TypeError:
        return "Число предпочтений должно быть числом!", 500
    if len(interests) == 0:
        return []
    if num_of_ideas not in range(1, 11):
        return "Не поддерживается число меньше 0 или больше 10!", 500
    if type(price_range) is not list:
        return "Ценовой диапазон должен быть списком!", 500
    if len(price_range) != 2:
        return "Ценовой диапазон может содержать лишь 2 значения!", 500
    try:
        price_range = [int(price_range[0]), int(price_range[1])]
    except TypeError:
        return "Ценовой диапазон должен быть задан числами!", 500
    return generate_ideas(interests, num_of_ideas, price_range)
