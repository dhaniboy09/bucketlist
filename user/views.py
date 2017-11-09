from flask import Blueprint

from user.api import UserAPI

user_app = Blueprint('user_app', __name__)

user_view = UserAPI.as_view('user_api')
user_app.add_url_rule('/users/', defaults={'user_id': None},
                      view_func=user_view, methods=['GET', ])
user_app.add_url_rule('/users/', view_func=user_view, methods=['POST', ])
user_app.add_url_rule('/users/<user_id>', view_func=user_view,
                      methods=['GET', 'PUT', 'DELETE', ])
