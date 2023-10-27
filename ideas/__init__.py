from flask import Blueprint
from .model import IdeaGenerator

idea = Blueprint('idea', __name__)
idea_generator = IdeaGenerator()

from . import views
