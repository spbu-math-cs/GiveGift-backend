from .DBMain import UserDatabase

data_base: UserDatabase = UserDatabase(database='sqlite:///user.db')
data_base.set_up_db()
