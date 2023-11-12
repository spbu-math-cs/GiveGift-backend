from flask import request

from core import app
from . import idea_generator


@app.route('/generate_ideas', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        interests = request.json.get("interests", None)
        num_of_ideas = request.json.get("num_of_ideas", None)
        price_range = request.json.get("price_range", None)
        if interests is None or num_of_ideas is None or price_range is None:
            return {"response": "500", "message": "4011"}
        if type(interests) is not list:
            return {"response": "500", "message": "4012"}
        try:
            num_of_ideas = int(num_of_ideas)
        except TypeError:
            return {"response": "500", "message": "4013"}
        if num_of_ideas not in range(1, 11):
            return {"response": "500", "message": "4014"}
        if type(price_range) is not list:  # price interval is list, contains two integers
            return {"response": "500", "message": "4014"}
        if len(price_range) != 2:
            return {"response": "500", "message": "4015"}
        try:
            price_interval = [int(price_range[0]), int(price_range[1])]
        except TypeError:
            return {"response": "500", "message": "4016"}
        return idea_generator.generate_ideas(interests, num_of_ideas, price_interval)
    if idea_generator.has_previous_ideas():
        return idea_generator.get_previous_ideas()
    return {}
