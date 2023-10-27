from flask import request
from flask_jwt_extended import jwt_required

from core import app
from core import idea_generator


@app.route('/generate_ideas', methods=["GET", "POST"])
#@jwt_required()
def index():
    if request.method == 'POST':
        interests = request.json.get("interests", None)
        num_of_ideas = request.json.get("num_of_ideas", None)
        price_interval = request.json.get("price_interval", None)
        if interests is None or num_of_ideas is None or price_interval is None:
            return {"response": "500", "message": "401"}
        if type(interests) is not list:
            return {"response": "500", "message": "401"}
        try:
            num_of_ideas = int(num_of_ideas)
        except TypeError:
            return {"response": "500", "message": "401"}
        if type(price_interval) is not list:  # price interval is list, contains two integers
            return {"response": "500", "message": "401"}
        if len(price_interval) != 2:
            return {"response": "500", "message": "401"}
        try:
            price_interval = [int(price_interval[0]), int(price_interval[1])]
        except TypeError:
            return {"response": "500", "message": "401"}
        return idea_generator.generate_ideas(interests, num_of_ideas, price_interval)
    if idea_generator.has_previous_ideas():
        return idea_generator.get_previous_ideas()
    return {}
