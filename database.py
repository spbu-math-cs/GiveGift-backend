import datetime

import sqlalchemy
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, func, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.exc import DatabaseError
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# TODO: make a class for all this

class DatabaseExitException(Exception):
    """
    Базовая ошибка, выбрасываемая функциями файла.
    """
    pass


def _raises_database_exit_exception(func):
    """
    Декоратор для внутренних функций, преобразующий DatabaseError в DatabaseExitException.
    :param func: Декорируемая функция.
    """

    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseError as e:
            raise DatabaseExitException(f"Невозможно получить данные из БД:\n{e}")

    return _wrapper


# TODO: add exception handling

class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Interest(db.Model):
    __tablename__ = "Interest"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(64), index=True, unique=True)

    def __repr__(self):
        return "<Interest '{}'>".format(self.name)


class User(UserMixin, db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    birth_date = db.Column(db.DateTime, index=True)
    about = db.Column(db.String(500), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.nickname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


user_interest_m2m = db.Table(
    "user_interest",
    sa.Column("user_id", sa.ForeignKey(User.id), primary_key=True),
    sa.Column("interest_id", sa.ForeignKey(Interest.id), primary_key=True)
)


# TODO: check why foreign keys work so bad


@_raises_database_exit_exception
def create_tables():
    with app.app_context():
        db.create_all()


@_raises_database_exit_exception
def drop_tables():
    with app.app_context():
        db.drop_all()


@_raises_database_exit_exception
def add_user(nickname: str, email: str, birth_date: datetime.datetime, about: str, password: str):
    with app.app_context():
        user = User()
        user.nickname = nickname
        user.about = about
        user.set_password(password)
        user.email = email
        user.birth_date = birth_date
        db.session.add(user)
        db.session.commit()


@_raises_database_exit_exception
def add_interest(name: str):
    with app.app_context():
        interest = Interest(name=name)
        db.session.add(interest)
        db.session.commit()


@_raises_database_exit_exception
def add_interest_to_user(user_id: int, interest_id: int):
    with app.app_context():
        db.session.execute(sa.insert(user_interest_m2m).values(user_id=user_id, interest_id=interest_id))
        db.session.commit()


@_raises_database_exit_exception
def delete_user_interest(user_id: int, interest_id: int):
    with app.app_context():
        db.session.execute(sa.delete(user_interest_m2m).where(and_(
            user_interest_m2m.c.user_id == user_id, user_interest_m2m.c.interest_id == interest_id)))
        db.session.commit()


@_raises_database_exit_exception
def delete_user_by_id(user_id: int):
    with app.app_context():
        clear_user_interests(user_id)
        User.query.filter_by(id=user_id).delete()
        db.session.commit()


@_raises_database_exit_exception
def delete_interest_by_id(interest_id: int):
    with app.app_context():
        db.session.execute(sa.delete(user_interest_m2m).where(user_interest_m2m.c.interest_id == interest_id))
        Interest.query.filter_by(id=interest_id).delete()
        db.session.commit()


@_raises_database_exit_exception
def get_user_by_id(user_id: int):
    with app.app_context():
        user = User.query.get(user_id)
        return user


@_raises_database_exit_exception
def get_user_by_nickname(nickname: str):
    with app.app_context():
        user = User.query.filter_by(nickname=nickname).first()
        return user


@_raises_database_exit_exception
def get_user_by_email(email: str):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        return user


@_raises_database_exit_exception
def get_interest_by_id(interest_id: int):
    with app.app_context():
        interest = Interest.query.filter_by(id=interest_id).first()
        return interest


@_raises_database_exit_exception
def get_interest_by_name(name: str):
    with app.app_context():
        interest = Interest.query.filter_by(name=name).first()
        return interest


@_raises_database_exit_exception
def get_count_of_users():
    with app.app_context():
        return User.query.count()


@_raises_database_exit_exception
def get_count_of_interests():
    with app.app_context():
        return Interest.query.count()


@_raises_database_exit_exception
def get_all_users():
    with app.app_context():
        return User.query.all()


@_raises_database_exit_exception
def get_all_interests():
    with app.app_context():
        return Interest.query.all()


@_raises_database_exit_exception
def get_user_interests(user_id: int):
    with app.app_context():
        select = db.session.execute(
            sa.select(user_interest_m2m.c.interest_id).where(
                user_interest_m2m.c.user_id == user_id)).fetchall()
        interests = []
        for interest_id in select:
            interests.append(Interest.query.filter_by(id=interest_id[0]).first())
        return interests


@_raises_database_exit_exception
def get_users_with_interest(interest_id: int):
    with app.app_context():
        select = db.session.execute(
            sa.select(user_interest_m2m.c.user_id).where(
                user_interest_m2m.c.interest_id == interest_id)).fetchall()
        users = []
        for user_id in select:
            users.append(User.query.filter_by(id=user_id[0]).first())
        return users


@_raises_database_exit_exception
def clear_user_interests(user_id: int):
    with app.app_context():
        db.session.execute(sa.delete(user_interest_m2m).where(user_interest_m2m.c.user_id == user_id))
        db.session.commit()


@_raises_database_exit_exception
def has_user(email: str, password: str):
    with app.app_context():
        user = get_user_by_email(email)
        if user is None:
            return False
        return user.check_password(password)


@_raises_database_exit_exception
def has_tag(tag: str):
    with app.app_context():
        return tag in list(map(lambda x: x.name, Interest.query.all()))


@_raises_database_exit_exception
def set_to_user_with_id(user_id: int, nickname: str, email: str, birth_date: datetime.datetime,
                        about: str, password: str):
    with app.app_context():
        db.session.query(User).filter_by(id=user_id).update({
            'nickname': nickname,
            'email': email,
            'birth_date': birth_date,
            'about': about,
            'password_hash': generate_password_hash(password)
        }, synchronize_session=False)
        db.session.commit()
