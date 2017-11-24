from flask.views import MethodView
from flask import jsonify, request, abort
from jsonschema import Draft4Validator
from jsonschema.exceptions import best_match
import uuid
import json
import datetime

from app.decorators import app_required
from user.decorators import user_required
from user.helpers import decode_jwt_token
from bucketlist.models import Bucketlist
from bucketlist.schema import schema
from bucketlist.templates import bucketlist_obj, bucketlist_objs
from user.models import User


class BucketlistAPI(MethodView):

    decorators = [app_required, user_required]

    def __init__(self):
        self.ITEMS_PER_PAGE = 10
        if (request.method != 'GET' and request.method != 'DELETE') and not request.json:
            abort(400)

    def get(self, bucketlist_item_id):
        if bucketlist_item_id:
            bucketlist_item = Bucketlist.objects.filter(external_id=bucketlist_item_id, live=True).first()
            if bucketlist_item:
                response = {
                    "status": "success",
                    "bucketlist_item": bucketlist_obj(bucketlist_item)
                }
                return jsonify(response), 200
            else:
                return jsonify({}), 404
        else:
            bucketlist_items = Bucketlist.objects.filter(live=True)
            page = int(request.args.get('page', 1))
            bucketlist_items = bucketlist_items.paginate(page=page, per_page=self.ITEMS_PER_PAGE)
            response = {
                "result": "ok",
                "links": [
                    {
                        "href": "/items/?page=%s" % page,
                        "rel": "self"
                    }
                ],
                "bucketlist_items": bucketlist_objs(bucketlist_items)
            }
            if bucketlist_items.has_prev:
                response["links"].append(
                    {
                        "href": "/items/?page=%s" % (bucketlist_items.prev_num),
                        "rel": "previous"
                    }
                )
            if bucketlist_items.has_next:
                response["links"].append(
                    {
                        "href": "/items/?page=%s" % (bucketlist_items.next_num),
                        "rel": "next"
                    }
                )
            return jsonify(response), 200

    def post(self):
        bucketlist_item_json = request.json
        error = best_match(Draft4Validator(schema).iter_errors(bucketlist_item_json))
        if error:
            return jsonify({"error": error.message}), 400
        user_token = request.headers.get('X-USER-TOKEN')
        user_id = decode_jwt_token(user_token)
        user = User.objects.filter(external_id=user_id).first()
        if not user:
            error = {
                "status": "fail",
                "message": "User Not Found"
            }
            return jsonify({'error': error}), 400

        created_on = datetime.datetime.utcnow()

        bucketlist_item = Bucketlist(
            external_id=str(uuid.uuid4()),
            name=bucketlist_item_json.get('name'),
            user=user,
            created_on=created_on
        ).save()
        response = {
            "status": "success",
            "message": "Bucket List Item Created",
            "bucketlist_item": bucketlist_obj(bucketlist_item)
        }
        return jsonify(response), 201

    def put(self, bucketlist_item_id):
        bucketlist_item = Bucketlist.objects.filter(external_id=bucketlist_item_id, live=True).first()
        if not bucketlist_item:
            return jsonify({}), 404
        bucketlist_item_json = request.json
        error = best_match(Draft4Validator(schema).iter_errors(bucketlist_item_json))
        if error:
            return jsonify({"error": error.message}), 400
        user_token = request.headers.get('X-USER-TOKEN')
        user_id = decode_jwt_token(user_token)
        if bucketlist_item.user.external_id == user_id:
            user = User.objects.filter(external_id=user_id, live=True).first()
            if not user:
                error = {
                    "status": "fail",
                    "message": "User Not Found"
                }
                return jsonify({'error': error}), 400
            modified_on = datetime.datetime.utcnow()
            bucketlist_item.name = bucketlist_item_json.get('name')
            bucketlist_item.modified_on = modified_on
            bucketlist_item.save()
            response = {
                "status": "success",
                "message": "Item Updated Successfully",
                "bucketlist_item": bucketlist_obj(bucketlist_item)
            }
            return jsonify(response), 200
        else:
            error = {
                "status": "fail",
                "message": "Unauthorized"
            }
            return jsonify({'error': error}), 403

    def delete(self, bucketlist_item_id):
        bucketlist_item = Bucketlist.objects.filter(external_id=bucketlist_item_id, live=True).first()
        if not bucketlist_item:
            return jsonify({}), 404
        user_token = request.headers.get('X-USER-TOKEN')
        user_id = decode_jwt_token(user_token)
        if bucketlist_item.user.external_id == user_id:
            bucketlist_item.live = False
            bucketlist_item.save()
            return jsonify({}), 204
        else:
            return jsonify({}), 403
