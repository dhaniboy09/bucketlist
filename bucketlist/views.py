from flask import Blueprint

from bucketlist.api import BucketListAPI

bucketlist_app = Blueprint('bucketlist_app', __name__)

bucketlist_view = BucketListAPI.as_view('bucketlist_api')
bucketlist_app.add_url_rule('/items/', defaults={'item_id': None},
                            view_func=bucketlist_view, methods=['GET', ])
bucketlist_app.add_url_rule('/items/', view_func=bucketlist_view, methods=['POST', ])
bucketlist_app.add_url_rule('/items/<int:item_id>', view_func=bucketlist_view,
                            methods=['GET', 'PUT', 'DELETE', ])

# bucketlist_app.add_url_rule('/items/', view_func=BucketListAPI.as_view('items'))
