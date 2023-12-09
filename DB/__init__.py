from .DB import UserDatabase

from .DBImitation import DataDecorator
data_base: DataDecorator = DataDecorator()

# data_base: UserDatabase = UserDatabase(database='sqlite:///user.db')
# data_base.create_tables()
