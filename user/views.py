from flask import Blueprint

from user.api import UserAPI, UserLoginView, UserSignUpView

user_app = Blueprint('user_app', __name__)

user_view = UserAPI.as_view('user_api')
signup_view = UserSignUpView.as_view('user_signup_view')
login_view = UserLoginView.as_view('user_login_view')

user_app.add_url_rule('/users/', defaults={'user_id': None},
                      view_func=user_view, methods=['GET', ])
user_app.add_url_rule('/users/<user_id>', view_func=user_view,
                      methods=['GET', 'PUT', 'DELETE', ])

user_app.add_url_rule('/users/', view_func=signup_view, methods=['POST', ])
user_app.add_url_rule('/users/login', view_func=login_view, methods=['POST', ])
