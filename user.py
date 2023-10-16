from flask import Flask
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# later: change to normal secret_key
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


# some functions to work with DB

class UsersProvider:
    time = datetime.now()

    class UserTagLists:
        def __init__(self, user: User, tag_list: list):
            self.user = user
            self.tag_list = tag_list

    __list_of_tag = [
        {"id": 0, "title": "Apple", "created": time, "description": "She loves big red apples."},
        {"id": 1, "title": "Kitten", "created": time, "description": "She loves small black kittens with black eyes."}
    ]

    __user_to_list_of_tag = {
        0: UserTagLists(User("USER_1", 0).hash_password("123"), __list_of_tag)
    }

    __users_login_to_index = {
        "USER_1": 0
    }

    __max_existing_user_index = 0

    @staticmethod
    def create_new_user(login: str, password: str):
        UsersProvider.__max_existing_user_index += 1
        user = User(name=login, id=UsersProvider.__max_existing_user_index).hash_password(password)
        UsersProvider.__users_login_to_index[login] = UsersProvider.__max_existing_user_index
        UsersProvider.__user_to_list_of_tag[UsersProvider.__max_existing_user_index] = UsersProvider.UserTagLists(user, [])

    @staticmethod
    def get_count_of_users():
        return UsersProvider.__max_existing_user_index + 1

    @staticmethod
    def delete_user(user_name: str):
        del UsersProvider.__user_to_list_of_tag[UsersProvider.__users_login_to_index[user_name]]
        del UsersProvider.__users_login_to_index[user_name]

    @staticmethod
    def get_user_by_name(name: str) -> User:
        try:
            return UsersProvider.__user_to_list_of_tag[UsersProvider.__users_login_to_index[name]].user
        except KeyError:
            # noinspection PyTypeChecker
            return None  # correct behaviour for lib function

    @staticmethod
    def get_user_by_index(index_: int) -> User:
        try:
            return UsersProvider.__user_to_list_of_tag[index_].user
        except KeyError:
            # noinspection PyTypeChecker
            return None  # correct behaviour for lib function

    @staticmethod
    def get_user_tags(name: str) -> list:
        try:
            return UsersProvider.__user_to_list_of_tag[UsersProvider.__users_login_to_index[name]].tag_list
        except KeyError:  # correct behaviour for lib func
            # noinspection PyTypeChecker
            return None

    @staticmethod
    def get_user_max_tags_index(name: str) -> int:
        try:
            return len(UsersProvider.__user_to_list_of_tag[UsersProvider.__users_login_to_index[name]].tag_list)
        except KeyError:  # correct behaviour for lib func
            # noinspection PyTypeChecker
            return None


class DataDecorator:
    @staticmethod
    def get_current_preference(preference_id: int, user: str) -> dict:
        return UsersProvider.get_user_tags(user)[preference_id]

    @staticmethod
    def get_list_of_preferences(user: str) -> list:
        return UsersProvider.get_user_tags(user)

    @staticmethod
    def append_to_list_of_preferences(title, description, user: str):
        UsersProvider.get_user_tags(user).append(
            {
                "id": UsersProvider.get_user_max_tags_index(user),
                "title": title,
                "description": description,
                "created": datetime.now()
            }
        )

    @staticmethod
    def set_to_list_of_preferences(preference_id, title, description, user):
        UsersProvider.get_user_tags(user)[preference_id] = {
            "id": preference_id,
            "title": title,
            "created": datetime.now(),
            "description": description
        }

    @staticmethod
    def delete_preference(preference_id, user):
        del UsersProvider.get_user_tags(user)[preference_id]

    @staticmethod
    def get_list_of_products():
        return [
            {
                "id": 1,
                "name": "Cheese",
                "price": 5000.0,
                "image": "https://i.ytimg.com/vi/Aa-F6zqLmig/maxresdefault.jpg?9289889566",
                "link": "https://pythonstart.ru/datetime/kak-poluchit-tekuschee-vremya-python"
            },
            {
                "id": 2,
                "name": "Bread",
                "price": 10000.0,
                "image": "https://i.ytimg.com/vi/Aa-F6zqLmig/maxresdefault.jpg?9289889566",
                "link": "https://pythonstart.ru/datetime/kak-poluchit-tekuschee-vremya-python"
            },
            {
                "id": 3,
                "name": "Butter",
                "price": 20000.0,
                "image": "https://i.ytimg.com/vi/Aa-F6zqLmig/maxresdefault.jpg?9289889566",
                "link": "https://pythonstart.ru/datetime/kak-poluchit-tekuschee-vremya-python"
            },
        ]




# replace all to get a correct behavior (when DB will be ready)
