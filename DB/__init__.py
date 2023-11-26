# from .DB import UserDatabase

from .DBImitation import DataDecorator

data_base: DataDecorator = DataDecorator()
# data_base: UserDatabase = UserDatabase()
# data_base.create_tables()
