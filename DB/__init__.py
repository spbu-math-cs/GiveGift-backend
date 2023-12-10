from .DBInterface import DBInterface

from .DBImitation import DataDecorator

data_base: DataDecorator = DataDecorator()

# data_base: UserDatabase = DBInterface(database='sqlite:///user.db')
