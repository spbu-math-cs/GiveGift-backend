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
                "price": 229.0,
                "image": "https://luckclub.ru/images/luckclub/2022/02/lonre.jpg",
                "link": "https://lavka.yandex.ru/2/good/syr-klassicheskij-brest-litovsk-45percent-200-gram?utm_medium=cpc&utm_source=yasearch&utm_campaign=75172803.%5BLVK%5DDT_LUA-goal_RU-LEN-SPE_dsa_feed_restype-search_NU&utm_content=k50id%7C010000004742010_4742010%7Ccid%7C75172803%7Cgid%7C5269085635%7Caid%7C14873780718%7Cadp%7Cno%7Cpos%7Cpremium1%7Csrc%7Csearch_none%7Cdvc%7Cdesktop%7C%7Bdop%7D%7C&k50id=010000004742010_4742010&utm_term=.4742010&yclid=12221166082480668671"
            },
            {
                "id": 2,
                "name": "Bread",
                "price": 46.0,
                "image": "https://catherineasquithgallery.com/uploads/posts/2021-02/1613516814_52-p-fon-dlya-prezentatsii-na-temu-khleb-65.jpg",
                "link": "https://market-delivery.yandex.ru/retail/vernyj_obaij/product/5e572b45-1f29-4b1f-9880-719cacc31fdb?item=5e572b45-1f29-4b1f-9880-719cacc31fdb&placeSlug=vernyj_natashi_kovshovoj_8a_otsgi&utm_campaign=92856615.%5BDC%5DMX_Retail-goal_RU-SPE-SPB_Verniy_gallery_feed_search_NU&utm_content=14798483131&utm_medium=cpc&utm_source=yasearch&utm_term=Все%20товары%7C%7Cpid%7C4276635%7Caid%7C14798483131%7Ctype3%7Cdesktop%7Cnone%7Csearch&yclid=14599912940698075135"
            },
            {
                "id": 3,
                "name": "Butter",
                "price": 109.0,
                "image": "https://agromer-storage-public.storage.yandexcloud.net/st/images/1214/offers/2e273fa7-eeb8-45a8-b0c0-4149633b3c2a/e9132d906e6e3e797ebdd5a0bfd06742.jpg",
                "link": "https://lavka.yandex.ru/2/good/maslo-sladko-slivochnoe-825percent-brest-litovsk-120-gram?utm_medium=cpc&utm_source=yasearch&utm_campaign=75172803.%5BLVK%5DDT_LUA-goal_RU-LEN-SPE_dsa_feed_restype-search_NU&utm_content=k50id%7C010000004742010_4742010%7Ccid%7C75172803%7Cgid%7C5269085635%7Caid%7C14873780718%7Cadp%7Cno%7Cpos%7Cpremium1%7Csrc%7Csearch_none%7Cdvc%7Cdesktop%7C%7Bdop%7D%7C&k50id=010000004742010_4742010&utm_term=.4742010&yclid=570279347904315391"
            },
        ]




# replace all to get a correct behavior (when DB will be ready)
