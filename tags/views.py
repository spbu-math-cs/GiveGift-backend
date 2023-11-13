from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from DB import data_base
from core import app


@app.route('/get_all_interests', methods=["GET"])
def get_all_interests():
    return {"all_interests": data_base.get_tags()}


@app.route('/edit_interest', methods=["POST"])
@jwt_required()
def edit_interest():
    email: str = get_jwt_identity()
    if email != 'ADMIN':
        return {"response": "500", "message": "401"}
    if not data_base.get_user_by_name_or_none(email).is_token_actual:
        return {"response": "500", "message": "Token is not actual"}

    new_interests = request.json.get("new_interests", "")
    edit_interests = request.json.get("edit_interests", "")
    if new_interests == "" or edit_interests == "":
        return {"response": "500", "message": "401"}
    if type(new_interests) is not list or type(edit_interests) is not list:
        return {"response": "500", "message": "401"}
    for interest in new_interests:
        if type(interest) is not str or data_base.has_tag(interest):
            return {"response": "500", "message": "401"}
        data_base.create_tag(interest)
    for interest in edit_interests:
        try:
            old_interest = interest["interest_name"]
            new_interest = interest["new_name"]
            if type(old_interest) is not str or type(new_interest) is not str:
                return {"response": "500", "message": "401"}
            if not data_base.has_tag(old_interest) or data_base.has_tag(new_interest):
                return {"response": "500", "message": "401"}
            data_base.delete_tag_as(old_interest)
            if new_interest != "":
                data_base.create_tag(new_interest)
            return {"response": "200", "message": "OK"}
        except TypeError:
            return {"response": "500", "message": "401"}
    return {"response": "200", "message": "OK"}
