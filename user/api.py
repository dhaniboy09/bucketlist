from flask.views import MethodView
from flask import jsonify, request, abort, render_template
import uuid
import json
import bcrypt
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match

from app.decorators import app_required
from user.models import User
from user.schema import schema, update_schema
from user.templates import user_obj, users_obj


class UserAPI(MethodView):
    decorators = [app_required]

    def __init__(self):
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
            response = {
                "result": "ok",
                "users": users_obj(users)
            }
            return jsonify(response), 200

    def post(self):
        user_json = request.json
        # This compares the request object with the schema validator (in schema.py)
        # and returns errors if any
        error = best_match(Draft4Validator(schema).iter_errors(user_json))
        if error:
            return jsonify({"error": error.message}), 400
        else:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user_json.get('password'), salt)
            user = User(
                external_id=str(uuid.uuid4()),
                first_name=user_json.get('first_name'),
                last_name=user_json.get('last_name'),
                email=user_json.get('email'),
                password=hashed_password
            ).save()
        response = {
            "result": "ok",
            "user": user_obj(user)
        }
        return jsonify(response), 201

    def put(self, user_id):
        user = User.objects.filter(external_id=user_id, live=True).first()
        if not user:
            return jsonify({}), 404
        user_json = request.json
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

    def delete(self, user_id):
        user = User.objects.filter(external_id=user_id, live=True).first()
        if not user:
            return jsonify({}), 404
        user.live = False
        user.save()
        return jsonify({}), 204
