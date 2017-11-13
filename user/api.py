from flask.views import MethodView
from flask import jsonify, request, abort, render_template
import uuid
import json
import jwt
import bcrypt
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match
from mongoengine import NotUniqueError
from datetime import datetime, timedelta

from app.decorators import app_required
from user.decorators import user_required
from user.models import User
from user.schema import schema, update_schema, password_schema
from user.templates import user_obj, users_obj
from user.helpers import encode_jwt_token


class UserAPI(MethodView):
    decorators = [app_required, user_required]

    def __init__(self):
        self.USERS_PER_PAGE = 10
        # If it's a POST or PUT request, it must come with a payload
        if (request.method != 'GET' and request.method != 'DELETE') and not request.json:
            abort(400)

    def get(self, user_id):
        if user_id:
            user = User.objects.filter(external_id=user_id, live=True).first()
            if user:
                response = {
                    "result": "ok",
                    "user": user_obj(user)
                }
                return jsonify(response), 200
            else:
                return jsonify({}), 404
        else:
            users = User.objects.filter(live=True)
            page = int(request.args.get('page', 1))
            users = users.paginate(page=page, per_page=self.USERS_PER_PAGE)
            print(users.items)
            response = {
                "result": "ok",
                "links": [
                    {
                        "href": "/users/?page=%s" % page,
                        "rel": "self"
                    }
                ],
                "users": users_obj(users)
            }
            if users.has_prev:
                response["links"].append(
                    {
                        "href": "/users/?page=%s" % (users.prev_num),
                        "rel": "previous"
                    }
                )
            if users.has_next:
                response["links"].append(
                    {
                        "href": "/users/?page=%s" % (users.next_num),
                        "rel": "previous"
                    }
                )
            return jsonify(response), 200

    def put(self, user_id):
        user = User.objects.filter(external_id=user_id, live=True).first()
        if not user:
            return jsonify({}), 404
        user_json = request.json
        if user_json.get('password'):
            error = best_match(Draft4Validator(password_schema).iter_errors(user_json))
            if error:
                return jsonify({"error": error.message}), 400
            else:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(user_json.get('password'), salt)
                user.password = hashed_password
                user.save()
                response = {
                    "result": "ok"
                }
                return jsonify(response), 200
        else:
            try:
                error = best_match(Draft4Validator(update_schema).iter_errors(user_json))
                if error:
                    return jsonify({"error": error.message}), 400
                else:
                    user.first_name = user_json.get('first_name')
                    user.last_name = user_json.get('last_name')
                    user.email = user_json.get('email')
                    user.save()
                    response = {
                        "result": "ok",
                        "user": user_obj(user)
                    }
                    return jsonify(response), 200
            except NotUniqueError:
                return jsonify({"error": "Email already in use"}), 400

    def delete(self, user_id):
        user = User.objects.filter(external_id=user_id, live=True).first()
        if not user:
            return jsonify({}), 404
        user.live = False
        user.save()
        return jsonify({}), 204


class UserLoginView(MethodView):
    decorators = [app_required]

    def __init__(self):
        if not request.json:
            abort(400)

    def post(self):
        if "email" not in request.json or "password" not in request.json:
            response = {
                "status": "fail",
                "message": "Missing Parameter"
            }
            return jsonify({'response': response}), 400
        user_json = request.json
        # Check if the user exists
        user = User.objects.filter(email=user_json.get('email')).first()
        if not user:
            response = {
                "status": "fail",
                "message": "User does not exist"
            }
            return jsonify({'response': response}), 400
        else:
            # check that the passwords match
            if bcrypt.hashpw(user_json.get('password'), user.password) == user.password:
                # create a login token
                user_token = encode_jwt_token(user.external_id)
                response = {
                    "status": "success",
                    "message": "Login successful",
                    "token": user_token.decode()
                }
                return jsonify({'response': response}), 200
            else:
                response = {
                    "status": "fail",
                    "message": "Incorrect Password"
                }
                return jsonify({'response': response}), 400


class UserSignUpView(MethodView):
    decorators = [app_required]

    def __init__(self):
        if not request.json:
            abort(400)

    def post(self):
        user_json = request.json
        # This compares the request object with the schema validator (in schema.py)
        # and returns errors if any
        error = best_match(Draft4Validator(schema).iter_errors(user_json))
        if error:
            return jsonify({"error": error.message}), 400
        else:
            try:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(user_json.get('password'), salt)
                user = User(
                    external_id=str(uuid.uuid4()),
                    first_name=user_json.get('first_name'),
                    last_name=user_json.get('last_name'),
                    email=user_json.get('email'),
                    password=hashed_password
                ).save()
                user_token = encode_jwt_token(user.external_id)
                response = {
                    "result": "ok",
                    "user": user_obj(user),
                    "user_token": user_token.decode()
                }
                return jsonify(response), 201
            except NotUniqueError:
                return jsonify({"error": "User already Exists"}), 400
