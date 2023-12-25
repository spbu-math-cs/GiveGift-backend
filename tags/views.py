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
    user = data_base.get_user_by_email_or_none(email)
    if not user.is_token_actual:
        return "Token is not actual!", 401
    if not user.is_admin:
        return "Только Админ может редактировать тэги!", 400
    new_interests = request.json.get("new_interests", "")
    edit_interests = request.json.get("edit_interests", "")
    if new_interests == "" or edit_interests == "":
        return "Логическая ошибка! Такого быть не должно! Плохо парсим тэги!", 400
    if type(new_interests) is not list or type(edit_interests) is not list:
        return "Логическая ошибка! Такого быть не должно! Плохо парсим тэги!", 400
    for interest in new_interests:
        if type(interest) is not str:
            return "Неверный тип тэга!", 400
        if data_base.has_tag(interest):
            return "Новый тэг не так уж и нов!", 400
        if interest == "":
            return "Недопустимое имя тэга!", 400
        data_base.add_tag(interest)
    for interest in edit_interests:
        try:
            old_interest = interest["interest_name"]
            new_interest = interest["new_name"]
            if type(old_interest) is not str or type(new_interest) is not str:
                return "Неверный тип тэга!", 400
            if not data_base.has_tag(old_interest):
                return "Старый тэг отсутствует в базе!", 400
            if data_base.has_tag(new_interest):
                return "Новый тэг есть в базе!", 400
            data_base.delete_tag(old_interest)
            if new_interest != "":
                data_base.add_tag(new_interest)
            return "OK", 200
        except TypeError:
            return "Неверный тип тэга!", 400
    return "OK", 200


@app.route('/add_admin', methods=["POST"])
@jwt_required()
def add_admin():
    email: str = get_jwt_identity()
    user = data_base.get_user_by_email_or_none(email)
    if not user.is_token_actual:
        return "Token is not actual!", 401
    if not user.is_admin:
        return "Только Админ может добавлять новых администраторов!", 400
    new_admin_id = request.json.get("id", "")
    try:
        new_admin_id = int(new_admin_id)
    except ValueError:
        return "ID не является числом!", 400
    user = data_base.get_user_by_index_or_none(new_admin_id)
    if user is None:
        return "Не существует пользователя с таким ID!", 500
    if user.is_admin or user.email == 'ADMIN@ADMIN.su':
        return "Указанный пользователь уже является администратором!", 500
    data_base.set_user_admin_as(user_id=new_admin_id, status=True)


@app.route('/delete_admin', methods=["POST"])
@jwt_required()
def delete_admin():
    email: str = get_jwt_identity()
    user = data_base.get_user_by_email_or_none(email)
    if not user.is_token_actual:
        return "Token is not actual!", 401
    if not user.is_admin:
        return "Только Админ может удалять администраторов!", 400
    new_admin_id = request.json.get("id", "")
    try:
        new_admin_id = int(new_admin_id)
    except ValueError:
        return "ID не является числом!", 400
    user = data_base.get_user_by_index_or_none(new_admin_id)
    if user is None:
        return "Не существует пользователя с таким ID!", 500
    if not user.is_admin:
        return "Указанный пользователь не является администратором!", 500
    if user.email == 'ADMIN@ADMIN.su':
        return "Невозможно удалить ADMIN@ADMIN.su!", 500
    data_base.set_user_admin_as(user_id=new_admin_id, status=False)  # TODO add to database ADMIN@ADMIN.su
