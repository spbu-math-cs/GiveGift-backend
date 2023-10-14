from flask import Flask
from werkzeug.exceptions import abort
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

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
        # self.password_hash = pwd_context.encrypt(password)
        self.password_hash = generate_password_hash(password)
        return self

    def verify_password(self, password):
        # return pwd_context.verify(password, self.password_hash)
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        # s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        # return s.dumps({'id': self.id})
        pass

    @staticmethod
    def verify_auth_token(token):
        pass
        # serializer = Serializer(app.config['SECRET_KEY'])
        # try:
        #     pass
            # data = serializer.loads(token)
        # except SignatureExpired:
        #     return None  # valid token, but expired
        # except BadSignature:
        #     return None  # invalid token
        # user = user_to_list_of_tag[data['id']][0]
        # return user

# some functions to work with DB


list_of_tag = [
    {"id": 0, "title": "Apple", "created": time, "description": "She loves big red apples."},
    {"id": 1, "title": "Kitten", "created": time, "description": "She loves small black kittens with black eyes."}
]

user_to_list_of_tag = [
    (User("USER_1", 0).hash_password("123"), list_of_tag)
]

users_login_to_index = {
    "USER_1": 0
}


class UsersGetter:
    @staticmethod
    def get_user_by_name(name: str) -> User:
        try:
            return user_to_list_of_tag[users_login_to_index[name]][0]
        except KeyError:
            # noinspection PyTypeChecker
            return None  # correct behaviour for lib function

    @staticmethod
    def get_user_by_index(index_: int) -> User:
        return user_to_list_of_tag[index_][0]

    @staticmethod
    def get_user_tags(name: str) -> list:
        try:
            return user_to_list_of_tag[users_login_to_index[name]][1]
        except KeyError:  # correct behaviour for lib func
            # noinspection PyTypeChecker
            return None


def get_current_preference(preference_id: int, user="USER_1"):
    return UsersGetter.get_user_tags(user)[preference_id]


def get_list_of_preferences(user="USER_1"):
    return UsersGetter.get_user_tags(user)


def append_to_list_of_preferences(title, description, user="USER_1"):
    UsersGetter.get_user_tags(user).append(
            {
                "id": len(list_of_tag),
                "title": title,
                "description": description,
                "created": datetime.now()
            }
        )


def set_to_list_of_preferences(preference_id, title, description, user="USER_1"):
    user_to_list_of_tag[users_login_to_index[user]][0][preference_id] = {
                "id": preference_id,
                "title": title,
                "created": datetime.now(),
                "description": description
            }


def delete_preference(preference_id, user="USER_1"):
    del UsersGetter.get_user_tags(user)[preference_id]


# replace all to get a correct behavior (when DB will be ready)

def get_tag(tag_id, user="USER_1"):
    try:
        current_preference = get_current_preference(tag_id, user)
        return current_preference
    except IndexError:
        abort(404)
