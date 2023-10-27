from flask import Flask

app = Flask(__name__)

from tags import tags as tags_blueprint
app.register_blueprint(blueprint=tags_blueprint)

from account import account as account_blueprint
app.register_blueprint(blueprint=account_blueprint)

from ideas import idea as idea_blueprint
app.register_blueprint(blueprint=idea_blueprint)

