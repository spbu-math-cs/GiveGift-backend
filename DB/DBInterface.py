from .DB import UserDatabase, _raises_database_exit_exception, User
import datetime


class DBInterface(UserDatabase):
    def __init__(self, database):
        super().__init__(database)
        super().create_tables()

    @_raises_database_exit_exception
    def create_user(self, nickname: str, email: str, password: str, about: str, birth_date: datetime.date,
                    interests: list) -> None:
        super().create_user(nickname, email, datetime.datetime.combine(birth_date, datetime.datetime.min.time()), about,
                            password)
        user = super().get_user_by_email_or_none(email)
        for i in interests:
            if not super().has_tag(i):
                super().add_tag(i)
            super().add_user_tag(user.nickname, i)

    @_raises_database_exit_exception
    def get_user_by_email_or_none(self, email: str) -> User:
        return super().get_user_by_email_or_none(email)

    @_raises_database_exit_exception
    def get_user_by_index_or_none(self, user_id: int) -> User:
        return super().get_user_by_index_or_none(user_id)

    @_raises_database_exit_exception
    def set_to_user_with_id(self, user_id: int, about: str, email: str, interests: list, nickname: str, password: str,
                            birth_date: datetime.date) -> None:
        super().set_to_user_with_id(user_id, nickname, email,
                                    datetime.datetime.combine(birth_date, datetime.datetime.min.time()), about,
                                    password)

    @_raises_database_exit_exception
    def send_friend_request(self, from_user_id: int, to_user_id: int) -> None:
        super().send_friend_request(from_user_id, to_user_id)

    @_raises_database_exit_exception
    def remove_friend_request(self, from_user_id: int, to_user_id: int) -> None:
        super().remove_friend_request(from_user_id, to_user_id)

    @_raises_database_exit_exception
    def accept_friend_request(self, from_user_id: int, to_user_id: int) -> None:
        super().accept_friend_request(from_user_id, to_user_id)

    @_raises_database_exit_exception
    def remove_friend(self, user_id: int, friend_id: int) -> None:
        super().remove_friend(user_id, friend_id)

    @_raises_database_exit_exception
    def is_friend(self, user_id: int, friend_id: int) -> bool:
        return super().is_friend(user_id, friend_id)

    @_raises_database_exit_exception
    def has_outgoing_request(self, user_id: int, friend_id: int) -> bool:
        return super().has_outgoing_requests(user_id, friend_id)

    @_raises_database_exit_exception
    def has_incoming_request(self, user_id: int, friend_id: int) -> bool:
        return super().has_incoming_requests(user_id, friend_id)

    @_raises_database_exit_exception
    def get_friends(self, user_id: int) -> list:
        return super().get_friends(user_id)

    @_raises_database_exit_exception
    def get_incoming_requests(self, user_id: int) -> list:
        return super().get_incoming_requests(user_id)

    @_raises_database_exit_exception
    def get_outgoing_requests(self, user_id: int) -> list:
        return super().get_outgoing_requests(user_id)
