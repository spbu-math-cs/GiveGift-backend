from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.exc import DatabaseError


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


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class ItemDatabase:
    def __init__(self, engine=None):
        # TODO: hard coding is bad.
        engine = engine if engine is not None else create_engine("sqlite:///item.db")
        self.engine = engine

    @_raises_database_exit_exception
    def create_tables(self):
        Base.metadata.create_all(self.engine)

    @_raises_database_exit_exception
    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    @_raises_database_exit_exception
    def upload_item(self, name: str):
        item = Item(
            name=name
        )

        with Session(self.engine) as session:
            session.add(item)
            session.commit()

    @_raises_database_exit_exception
    def download_items(self):
        with Session(self.engine) as session:
            items = session.query(Item).all()
        return items
