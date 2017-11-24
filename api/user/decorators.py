from functools import wraps
from flask import request, jsonify
from datetime import datetime

from user.models import User
from user.helpers import decode_jwt_token


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_token = request.headers.get('X-USER-TOKEN')

        if user_token is None:
            return jsonify({}), 403

        # verify that user still exists
        payload = decode_jwt_token(user_token)
        user = User.objects.filter(external_id=payload).first()
        if not user:
            return jsonify({}), 403

        return f(*args, **kwargs)
    return decorated_function
