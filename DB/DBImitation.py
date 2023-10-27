from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


class User:
    __max_id = 0

    def __init__(self, nickname: str, email: str, birth_date: date, about: str, interests: list):
        self.id = User.__max_id + 1
        User.__max_id += 1
        self.nickname = nickname
        self.email = email
        self.password_hash = None
        self.birth_date = birth_date
        self.about = about
        self.interests = interests

    def hash_password(self, password: str):
        self.password_hash = generate_password_hash(password)
        return self

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_interest(self, interest: str):
        self.interests.append(interest)


# some functions to work with DB

class UsersProvider:
    def __init__(self):
        # noinspection PyTypeChecker
        self.__users = [User("TestNick", "ivan@login.su", None, None, []).hash_password("12345")]  # initialize DB

    def create_new_user(self, nickname: str, login: str, password: str, about: str, birth_date: date, interests: list):
        self.__users.append(User(nickname, login, birth_date, about, interests).hash_password(password))

    def get_count_of_users(self):
        return len(self.__users)

    def delete_user(self, user_name: str):
        del [user for user in self.__users if user.nickname == user_name][0]

    def get_user_by_name(self, user_name: str) -> User:
        try:
            return [user for user in self.__users if user.email == user_name][0]
        except KeyError:
            # noinspection PyTypeChecker
            return None  # correct behaviour for lib function

    def get_user_by_index(self, user_index: int) -> User:
        try:
            return [user for user in self.__users if user.id == user_index][0]
        except KeyError:
            # noinspection PyTypeChecker
            return None  # correct behaviour for lib function

    def get_user_tags(self, name: str) -> list:
        user = self.get_user_by_name(name)
        if user is None:
            # noinspection PyTypeChecker
            return None
        return user.interests


class TagProvider:
    def __init__(self):
        self.__interests = ["Films", "Images", "Driving", "Making project for Prog. Eng.", "Tinkoff", "Programming"]

    def get_interests(self):
        return self.__interests[:]

    def add_interests(self, interest: str):
        self.__interests.append(interest)

    def delete_interest(self, interest: str):
        self.__interests.remove(interest)


class DataDecorator:
    def __init__(self):
        self.__tag_provider = TagProvider()  # initialize DB
        self.__user_provider = UsersProvider()

    def has_user_as(self, login: str, password: str):
        user = self.__user_provider.get_user_by_name(login)
        if user is None:
            return False
        return user.verify_password(password)

    def has_tag_as(self, tag: str):
        return tag in self.__tag_provider.get_interests()

    def get_tags(self):
        return self.__tag_provider.get_interests()

    def get_tag_count(self):
        return len(self.__tag_provider.get_interests())

    def create_user(self, nickname: str, login: str, password: str, about: str, birth_date: date, interests: list):
        self.__user_provider.create_new_user(nickname, login, password, about, birth_date, interests)

    def get_user_by_name(self, name: str):
        return self.__user_provider.get_user_by_name(name)

    def has_user_with_id(self, user_id: int):
        return self.__user_provider.get_user_by_index(user_id) is not None

    def get_user_with_id(self, user_id: int):
        return self.__user_provider.get_user_by_index(user_id)

# replace all to get a correct behavior (when DB will be ready)
