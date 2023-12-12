import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


class User:
    __max_id = 0

    def __init__(self, nickname: str, email: str, birth_date: date, about: str, interests: list, password: str):
        self.id = User.__max_id + 1
        User.__max_id += 1
        self.nickname = nickname
        self.email = email
        self.__password_hash = generate_password_hash(password=password)
        self.birth_date = birth_date
        self.about = about
        self._interests = interests
        self.is_token_actual = False
        self.__friends = []
        self.__incoming_requests = []
        self.__outgoing_requests = []
        self.__messages = {}
        self.last_time_seen = datetime.datetime.now()
        self.__max_message_id = 0

    def _verify_password(self, password) -> bool:
        return check_password_hash(pwhash=self.__password_hash, password=password)

    # def add_user_tag(self, interest: str) -> None:
    #     self._interests.append(interest)

    def _add_friend(self, friend_id: int) -> None:
        if friend_id not in self.__friends:
            self.__friends.append(friend_id)
        else:
            raise AssertionError("Friend has already been added!")

    def _remove_friend(self, friend_id: int) -> None:
        if friend_id not in self.__friends:
            raise AssertionError("This user is not your friend!")
        else:
            self.__friends.remove(friend_id)

    def _is_friend(self, friend_id: int) -> bool:
        if friend_id in self.__friends:
            return True
        return False

    def _add_application(self, friend_id: int) -> None:
        if friend_id not in self.__friends:
            self.__outgoing_requests.append(friend_id)
        else:
            raise AssertionError("Friend has already been added!")

    def _remove_application(self, friend_id: int) -> None:
        if friend_id not in self.__outgoing_requests:
            raise AssertionError("This user is not your friend!")
        else:
            self.__outgoing_requests.remove(friend_id)

    def _has_application(self, friend_id: int) -> bool:
        if friend_id in self.__outgoing_requests:
            return True
        return False

    def _add_potential_friend(self, friend_id: int) -> None:
        if friend_id not in self.__incoming_requests:
            self.__incoming_requests.append(friend_id)
        else:
            raise AssertionError("Friend has already been added!")

    def _remove_potential_friend(self, friend_id: int) -> None:
        if friend_id not in self.__incoming_requests:
            raise AssertionError("This user is not your friend!")
        else:
            self.__incoming_requests.remove(friend_id)

    def _is_potential_friend(self, friend_id: int) -> bool:
        if friend_id in self.__incoming_requests:
            return True
        return False

    def _get_friends(self) -> list:
        return self.__friends[:]

    def _get_incoming_requests(self) -> list:
        return self.__incoming_requests[:]

    def _get_outgoing_requests(self) -> list:
        return self.__outgoing_requests[:]

    def _delete_message_with_id(self, message_id: int):
        if message_id in self.__messages.keys():
            del self.__messages[message_id]
        else:
            raise IndexError("Have not this id!")

    def _add_message(self, text: str, addition_date: datetime.datetime):
        self.__max_message_id += 1
        self.__messages[self.__max_message_id] = {
            "text": text,
            "addition_date": addition_date,
            "id": self.__max_message_id
        }

    def _get_messages(self):
        return self.__messages[:]

    def _has_message_with_id(self, message_id: int):
        return message_id in self.__messages.keys()

    @property
    def get_interests(self):
        return self._interests


# some functions to work with DB
class UsersProvider:
    def __init__(self):
        # noinspection PyTypeChecker
        self.__users = [
            User(
                nickname="TestNick",
                email="ivan@login.su",
                birth_date=None,
                about="",
                interests=[],
                password="12345"
            ),
            User(
                nickname="Amirelkanov",
                email="amirelkanov0504@gmail.com",
                birth_date=None,
                about="",
                interests=['Тест'],
                password="123"
            ),
            User(
                nickname="Test",
                email="amirelkanov@yandex.ru",
                birth_date=None,
                about="",
                interests=['Тест'],
                password="123"
            )
        ]
        # initialize DB

    def _create_user(self, nickname: str, email: str, password: str, about: str, birth_date: date, interests: list) -> None:
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

    # def get_count_of_users(self) -> int:
    #     return len(self.__users)

#     def delete_user(self, user_name: str) -> None:
#         if self.get_user_by_email_or_none(user_name) is None:
#             raise AssertionError("Can't delete user, that is not exists!")
#         del [user for user in self.__users if user.nickname == user_name][0]
# #
    def _get_user_by_email_or_none(self, email: str) -> User:
        try:
            return [user for user in self.__users if user.email == email][0]
        except IndexError:
            # noinspection PyTypeChecker
            return None

    def _get_user_by_index_or_none(self, user_id: int) -> User:
        try:
            return [user for user in self.__users if user.id == user_id][0]
        except IndexError:
            # noinspection PyTypeChecker
            return None

    # def get_user_tags_by_name(self, email: str) -> list:
    #     user = self.get_user_by_email_or_none(email=email)
    #     if user is None:
    #         raise AssertionError("Can't get user tags, if user is not exists!")
    #     return user._interests


class TagProvider:
    def __init__(self):
        self.__tags = ["Кино", "Мультфильмы", "Походы", "Романтика", "Цветы", "Духи", "Книги", "Спорт", "Природа"]

    def _get_tags(self) -> list:
        return self.__tags[:]

    def _add_tag(self, tag: str) -> None:
        if tag in self.__tags:
            raise AssertionError("Tag with this name_of_product was already added!")
        self.__tags.append(tag)

    def _delete_tag(self, tag: str) -> None:
        if tag not in self.__tags:
            raise AssertionError("Tag with this name_of_product wasn't already added!")
        self.__tags.remove(tag)


class DataDecorator:
    def __init__(self):
        self.__tag_provider = TagProvider()  # initialize DB
        self.__user_provider = UsersProvider()

    def has_user(self, email: str, password: str) -> bool:
        user = self.__user_provider._get_user_by_email_or_none(email=email)
        if user is None:
            return False
        return user._verify_password(password)

    def has_tag(self, tag: str) -> bool:
        return tag in self.__tag_provider._get_tags()

    def add_tag(self, tag: str) -> None:
        if self.has_tag(tag):
            raise AssertionError("Can't add tag, that is exists!")
        self.__tag_provider._add_tag(tag)

    def delete_tag(self, tag: str) -> None:
        if not self.has_tag(tag):
            raise AssertionError("Can't delete tag, that is not exists!")
        self.__tag_provider._delete_tag(tag)

    def get_tags(self) -> list:
        return self.__tag_provider._get_tags()

    def get_count_of_tags(self) -> int:
        return len(self.__tag_provider._get_tags())

    def create_user(self, nickname: str, email: str, password: str, about: str, birth_date: date, interests: list) -> None:
        if email is None or password is None:
            raise AssertionError("Can't create user without email or password!")
        self.__user_provider._create_user(nickname, email, password, about, birth_date, interests)

    def get_user_by_email_or_none(self, email: str) -> User:
        return self.__user_provider._get_user_by_email_or_none(email=email)

    def get_user_by_index_or_none(self, user_id: int) -> User:
        return self.__user_provider._get_user_by_index_or_none(user_id=user_id)

    def set_to_user_with_id(self, user_id: int, about: str, email: str, interests: list, nickname: str, password: str, birth_date: date) -> None:
        user = self.get_user_by_index_or_none(user_id)
        user.about = about
        user.email = email
        user.__interests = interests
        user.nickname = nickname
        user.birth_date = birth_date
        user.password = password

    def send_friend_request(self, from_user_id: int, to_user_id: int) -> None:
        from_user = self.get_user_by_index_or_none(from_user_id)
        to_user = self.get_user_by_index_or_none(to_user_id)
        if from_user._is_friend(to_user_id):
            raise RuntimeError("From_user already is friend of to_user!")
        from_user._add_application(to_user_id)
        to_user._add_potential_friend(from_user_id)

    def remove_friend_request(self, from_user_id: int, to_user_id: int) -> None:
        from_user = self.get_user_by_index_or_none(from_user_id)
        to_user = self.get_user_by_index_or_none(to_user_id)
        if not from_user._has_application(to_user_id):
            raise RuntimeError("From_user did not send request to to_user!")
        from_user._remove_application(to_user_id)
        to_user._remove_potential_friend(from_user_id)

    def accept_friend_request(self, from_user_id: int, to_user_id: int) -> None:
        from_user = self.get_user_by_index_or_none(from_user_id)
        to_user = self.get_user_by_index_or_none(to_user_id)
        if not to_user._is_potential_friend(from_user_id):
            raise RuntimeError("From_user don't want to tell with you!")
        if not from_user._has_application(to_user_id):
            raise RuntimeError("From_user don't want to tell with you!")
        to_user._remove_potential_friend(from_user_id)
        from_user._remove_application(to_user_id)
        from_user._add_friend(to_user_id)
        to_user._add_friend(from_user_id)

    def remove_friend(self, user_id: int, friend_id: int) -> None:
        user = self.get_user_by_index_or_none(user_id)
        user._remove_friend(friend_id)
        friend = self.get_user_by_index_or_none(friend_id)
        friend._remove_friend(user_id)

    def is_friend(self, user_id: int, friend_id: int) -> bool:
        user = self.get_user_by_index_or_none(user_id)
        return user._is_friend(friend_id)

    def has_outgoing_request(self, user_id: int, friend_id: int) -> bool:
        user = self.get_user_by_index_or_none(user_id)
        return user._has_application(friend_id)

    def has_incoming_request(self, user_id: int, friend_id: int) -> bool:
        user = self.get_user_by_index_or_none(user_id)
        return user._is_potential_friend(friend_id)

    def get_friends(self, user_id: int) -> list:
        user = self.get_user_by_index_or_none(user_id)
        return user._get_friends()

    def get_incoming_requests(self, user_id: int) -> list:
        user = self.get_user_by_index_or_none(user_id)
        return user._get_incoming_requests()

    def get_outgoing_requests(self, user_id: int) -> list:
        user = self.get_user_by_index_or_none(user_id)
        return user._get_outgoing_requests()

    def delete_message_with_id(self, user_id: int, message_id: int):
        user = self.get_user_by_index_or_none(user_id)
        user._delete_message_with_id(message_id)

    def add_message(self, user_id: int, text: str, addition_date: datetime.datetime):
        user = self.get_user_by_index_or_none(user_id)
        user._add_message(text, addition_date)

    def get_messages(self, user_id: int):
        return self.get_user_by_index_or_none(user_id)._get_messages()

    def has_message_with_id(self, user_id: int, message_id: int):
        return self.get_user_by_index_or_none(user_id)._has_message_with_id(message_id)

    def get_user_tags(self, user_id: int) -> list:
        return self.get_user_by_index_or_none(user_id)._interests[:]

    def set_user_token_as(self, user_id: int, value: bool):
        self.get_user_by_index_or_none(user_id).is_token_actual = value


# replace all to get a correct behavior (when DB will be ready)
