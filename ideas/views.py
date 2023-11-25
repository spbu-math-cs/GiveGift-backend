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
                return {"response": "500", "message": "4011"}  # TODO change error codes
            user = data_base.get_user_by_email_or_none(current_email)
            if not user.is_friend(friend_id):
                return {"response": "500", "message": "4011"}
            friend = data_base.get_user_with_id(friend_id)
            interests = str(friend.interests)
    if interests == "" or num_of_ideas == "" or price_range == "":
        return {"response": "500", "message": "4011"}
    if type(interests) is not list:
        return {"response": "500", "message": "4012"}
    try:
        num_of_ideas = int(num_of_ideas)
    except TypeError:
        return {"response": "500", "message": "4013"}
    if len(interests) == 0:
        return []
    if num_of_ideas not in range(1, 11):
        return {"response": "500", "message": "4014"}
    if type(price_range) is not list:
        return {"response": "500", "message": "4014"}
    if len(price_range) != 2:
        return {"response": "500", "message": "4015"}
    try:
        price_range = [int(price_range[0]), int(price_range[1])]
    except TypeError:
        return {"response": "500", "message": "4016"}
    return generate_ideas(interests, num_of_ideas, price_range)
