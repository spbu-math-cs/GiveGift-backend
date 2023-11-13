from flask import request

from core import app
from ideas.generator import generate_ideas


@app.route('/generate_ideas', methods=["POST"])
def index():
    interests = request.json.get("interests", "")
    num_of_ideas = request.json.get("num_of_ideas", "")
    price_range = request.json.get("price_range", "")
    if interests is "" or num_of_ideas is "" or price_range is "":
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
    if type(price_range) is not list:  # price interval is list, contains two integers
        return {"response": "500", "message": "4014"}
    if len(price_range) != 2:
        return {"response": "500", "message": "4015"}
    try:
        price_range = [int(price_range[0]), int(price_range[1])]
    except TypeError:
        return {"response": "500", "message": "4016"}

    return generate_ideas(interests, num_of_ideas, price_range)
