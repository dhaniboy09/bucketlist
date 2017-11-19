from flask import Blueprint

from bucketlist.api import BucketlistAPI

bucketlist_app = Blueprint('bucketlist_app', __name__)

bucketlist_view = BucketlistAPI.as_view('bucketlist_api')
bucketlist_app.add_url_rule('/items/', defaults={'bucketlist_item_id': None},
                            view_func=bucketlist_view, methods=['GET', ])
bucketlist_app.add_url_rule('/items/', view_func=bucketlist_view, methods=['POST', ])
bucketlist_app.add_url_rule('/items/<bucketlist_item_id>', view_func=bucketlist_view,
                            methods=['GET', 'PUT', 'DELETE', ])
