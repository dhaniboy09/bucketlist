from flask.views import MethodView
from flask import jsonify, request, abort


class BucketListAPI(MethodView):
    items = [
        {"id": 1, "name": u"Mac", "links": [{"rel": "self", "href": "/items/1"}]},
        {"id": 2, "name": u"Leo", "links": [{"rel": "self", "href": "/items/2"}]},
        {"id": 3, "name": u"Brownie", "links": [{"rel": "self", "href": "/items/1"}]}
    ]

    def get(self, item_id):
        if item_id:
            return jsonify({"item": self.items[item_id - 1]})
        else:
            return jsonify({"items": self.items})

    def post(self):
        if not request.json or 'name' not in request.json:
            abort(400)
        item = {
            "id": len(self.items) + 1,
            "name": request.json["name"],
            "links": [{"rel": "self", "href": "/items/" + str(len(self.items) + 1)}]
        }
        self.items.append(item)
        return jsonify({'item': item}), 201

    def put(self, item_id):
        if not request.json or 'name' not in request.json:
            abort(400)
        item = self.items[item_id - 1]
        item["name"] = request.json["name"]
        return jsonify({'item': item}), 200

    def delete(self, item_id):
        del self.items[item_id - 1]
        return jsonify({}), 204
