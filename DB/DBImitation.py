from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


class User:
    __max_id = 0

    def __init__(self, nickname: str, email: str, birth_date: date, about: str, interests: list, password: str):
        self.id = User.__max_id + 1
        User.__max_id += 1
        self.nickname = nickname
        self.email = email
        self.password_hash = generate_password_hash(password=password)
        self.birth_date = birth_date
        self.about = about
        self.interests = interests

    def verify_password(self, password) -> bool:
        return check_password_hash(pwhash=self.password_hash, password=password)

    def add_user_tag(self, interest: str) -> None:
        self.interests.append(interest)


# some functions to work with DB

class UsersProvider:
    def __init__(self):
        # noinspection PyTypeChecker
        self.__users = [
            User(
                nickname="TestNick",
                email="ivan@login.su",
                birth_date=None,
                about=None,
                interests=[],
                password="12345"
            )
        ]
        # initialize DB

    def create_user(self, nickname: str, email: str, password: str, about: str, birth_date: date, interests: list) -> None:
        self.__users.append(
            User(
                nickname=nickname,
                email=email,
                birth_date=birth_date,
                about=about,
                interests=interests,
                password=password
            )
        )

    def get_count_of_users(self) -> int:
        return len(self.__users)

    def delete_user(self, user_name: str) -> None:
        if self.get_user_by_name_or_none(user_name) is None:
            raise AssertionError("Can't delete user, that is not exists!")
        del [user for user in self.__users if user.nickname == user_name][0]

    def get_user_by_name_or_none(self, email: str) -> User:
        try:
            return [user for user in self.__users if user.email == email][0]
        except KeyError:
            # noinspection PyTypeChecker
            return None

    def get_user_by_index_or_none(self, user_id: int) -> User:
        try:
            return [user for user in self.__users if user.id == user_id][0]
        except KeyError:
            # noinspection PyTypeChecker
            return None

    def get_user_tags_by_name(self, email: str) -> list:
        user = self.get_user_by_name_or_none(email=email)
        if user is None:
            raise AssertionError("Can't get user tags, if user is not exists!")
        return user.interests


class TagProvider:
    def __init__(self):
        self.__tags = ["Films", "Images", "Driving", "Making project for Prog. Eng.", "Tinkoff", "Programming"]

    def get_tags(self) -> list:
        return self.__tags[:]

    def add_tag(self, tag: str) -> None:
        if tag in self.__tags:
            raise AssertionError("Tag with this name was already added!")
        self.__tags.append(tag)

    def delete_tag(self, tag: str) -> None:
        if tag not in self.__tags:
            raise AssertionError("Tag with this name wasn't already added!")
        self.__tags.remove(tag)


class DataDecorator:
    def __init__(self):
        self.__tag_provider = TagProvider()  # initialize DB
        self.__user_provider = UsersProvider()

    def has_user(self, email: str, password: str) -> bool:
        user = self.__user_provider.get_user_by_name_or_none(email=email)
        if user is None:
            return False
        return user.verify_password(password)

    def has_tag(self, tag: str) -> bool:
        return tag in self.__tag_provider.get_tags()

    def create_tag(self, tag: str) -> None:
        if self.has_tag(tag):
            raise AssertionError("Can't add tag, that is exists!")
        self.__tag_provider.add_tag(tag)

    def delete_tag_as(self, tag: str) -> None:
        if not self.has_tag(tag):
            raise AssertionError("Can't delete tag, that is not exists!")
        self.__tag_provider.delete_tag(tag)

    def get_tags(self) -> list:
        return self.__tag_provider.get_tags()

    def get_tags_count(self) -> int:
        return len(self.__tag_provider.get_tags())

    def create_user(self, nickname: str, email: str, password: str, about: str, birth_date: date, interests: list) -> None:
        if email is None or password is None:
            raise AssertionError("Can't create user without email or password!")
        self.__user_provider.create_user(nickname, email, password, about, birth_date, interests)

    def get_user_by_name_or_none(self, email: str) -> User:
        return self.__user_provider.get_user_by_name_or_none(email=email)

    def has_user_with_id(self, user_id: int) -> bool:
        return self.__user_provider.get_user_by_index_or_none(user_id=user_id) is not None

    def get_user_with_id(self, user_id: int) -> User:
        return self.__user_provider.get_user_by_index_or_none(user_id=user_id)

    def set_to_user_with_id(self, user_id: int, about: str, email: str, interests: list, nickname: str, password: str, birth_date: date) -> None:
        user = self.get_user_with_id(user_id)
        user.about = about
        user.email = email
        user.interests = interests
        user.nickname = nickname
        user.birth_date = birth_date
        user.password = password

# replace all to get a correct behavior (when DB will be ready)
