from flask import Blueprint

from user.api import UserAPI, UserLoginView, UserSignUpView

user_app = Blueprint('user_app', __name__)

user_view = UserAPI.as_view('user_api')
signup_view = UserSignUpView.as_view('user_signup_view')
login_view = UserLoginView.as_view('user_login_view')

# Get all users
user_app.add_url_rule('/users/', defaults={'user_id': None},
                      view_func=user_view, methods=['GET', ])
# Get a user's profile
user_app.add_url_rule('/users/<user_id>', view_func=user_view,
                      methods=['GET', 'PUT', 'DELETE', ])
# Register a new user
user_app.add_url_rule('/users/', view_func=signup_view, methods=['POST', ])
# Login a user
user_app.add_url_rule('/users/login', view_func=login_view, methods=['POST', ])
# Get a user's bucketlist
user_app.add_url_rule('/users/<user_id>/items/', view_func=user_view, methods=['GET', ])
