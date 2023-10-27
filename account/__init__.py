from flask import Blueprint

account = Blueprint('account', __name__, url_prefix='/account')

from . import views
