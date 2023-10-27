from flask import Flask
from .model import IdeaGenerator

app = Flask(__name__)
idea_generator = IdeaGenerator()

from tags import tags as tags_blueprint
app.register_blueprint(tags_blueprint)

from account import account as account_blueprint
app.register_blueprint(account_blueprint)

from ideas import idea as idea_blueprint
app.register_blueprint(idea_blueprint)

from core import views
