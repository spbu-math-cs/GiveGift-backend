from flask import Flask
from werkzeug.exceptions import abort
from datetime import datetime
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

app: Flask
time = datetime.now()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fkbvkfjbjfbldsovfmvbkfmbfkbkjhkgkkldksdlklfdlfkkprkppcpkfkpewp'


class User(UserMixin):
    # noinspection PyShadowingBuiltins
    def __init__(self, name: str, id: int):
        self.name = name
        self.password_hash = None
        self.id = id

    def hash_password(self, password: str):
        self.password_hash = generate_password_hash(password)
        return self

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def is_authenticated(self):
    #     return UsersGetter.get_user_by_name(self.name) is not None


# some functions to work with DB
class UserTagLists:
    def __init__(self, user: User, tag_list: list):
        self.user = user
        self.tag_list = tag_list


__list_of_tag = [
    {"id": 0, "title": "Apple", "created": time, "description": "She loves big red apples."},
    {"id": 1, "title": "Kitten", "created": time, "description": "She loves small black kittens with black eyes."}
]

user_to_list_of_tag = {
    0: UserTagLists(User("USER_1", 0).hash_password("123"), __list_of_tag)
}

users_login_to_index = {
    "USER_1": 0
}

max_existing_user_index = 0


class UsersGetter:
    @staticmethod
    def create_new_user(login: str, password: str):
        global max_existing_user_index
        max_existing_user_index += 1
        user = User(name=login, id=max_existing_user_index).hash_password(password)
        users_login_to_index[login] = max_existing_user_index
        user_to_list_of_tag[max_existing_user_index] = UserTagLists(user, [])

    @staticmethod
    def delete_user(user_name: str):
        del user_to_list_of_tag[users_login_to_index[user_name]]
        del users_login_to_index[user_name]

    @staticmethod
    def get_user_by_name(name: str) -> User:
        try:
            return  user_to_list_of_tag[users_login_to_index[name]].user
        except KeyError:
            # noinspection PyTypeChecker
            return None  # correct behaviour for lib function

    @staticmethod
    def get_user_by_index(index_: int) -> User:
        try:
            return user_to_list_of_tag[index_].user
        except KeyError:
            # noinspection PyTypeChecker
            return None  # correct behaviour for lib function

    @staticmethod
    def get_user_tags(name: str) -> list:
        try:
            return user_to_list_of_tag[users_login_to_index[name]].tag_list
        except KeyError:  # correct behaviour for lib func
            # noinspection PyTypeChecker
            return None

    @staticmethod
    def get_user_max_tags_index(name: str) -> int:
        try:
            return len(user_to_list_of_tag[users_login_to_index[name]].tag_list)
        except KeyError:  # correct behaviour for lib func
            # noinspection PyTypeChecker
            return None


def get_current_preference(preference_id: int, user: str) -> dict:
    return UsersGetter.get_user_tags(user)[preference_id]


def get_list_of_preferences(user: str) -> list:
    return UsersGetter.get_user_tags(user)


def append_to_list_of_preferences(title, description, user: str):
    UsersGetter.get_user_tags(user).append(
        {
            "id": UsersGetter.get_user_max_tags_index(user),
            "title": title,
            "description": description,
            "created": datetime.now()
        }
    )


def set_to_list_of_preferences(preference_id, title, description, user="USER_1"):
    user_to_list_of_tag[users_login_to_index[user]].tag_list[preference_id] = {
        "id": preference_id,
        "title": title,
        "created": datetime.now(),
        "description": description
    }


def delete_preference(preference_id, user):
    del UsersGetter.get_user_tags(user)[preference_id]


# replace all to get a correct behavior (when DB will be ready)

def get_tag(tag_id, user):
    try:
        current_preference = get_current_preference(tag_id, user)
        return current_preference
    except IndexError:
        abort(404)
