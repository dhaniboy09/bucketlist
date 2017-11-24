from application import create_app as create_app_base
from mongoengine.connection import _get_db
import unittest
import json
from datetime import datetime

from settings import MONGODB_HOST, MONGODB_DB
from bucketlist.models import Bucketlist
from application import fixtures


class BucketlistTest(unittest.TestCase):
    def create_app(self):
        self.db_name = 'bucketlist-api-test'
        return create_app_base(
            MONGODB_SETTINGS={'DB': self.db_name,
                              'HOST': MONGODB_HOST},
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY='mySecret!',
        )

    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

    def tearDown(self):
        db = _get_db()
        db.client.drop_database(db)

    def app_dict(self):
        return json.dumps(dict(
            app_id="user_client",
            app_secret="user_secret"
        ))

    def user_dict(self):
        return json.dumps(dict(
            first_name="Alex",
            last_name="Skarsgard",
            email="askar@yahoo.com",
            password="AndelaIssaSeriesC&123"
        ))

    def bucketlist_dict(self):
        return json.dumps(dict(
            name="Yearly Trip to the Maldives",
        ))

    def login_user_dict(self):
        return json.dumps(dict(
            email="askar@yahoo.com",
            password="AndelaIssaSeriesC&123"
        ))

    def create_api_app(self):
        # create our app
        rv = self.app.post('/apps/',
                           data=self.app_dict(),
                           content_type='application/json')

    def generate_access_token(self):
        # generate an access token
        rv = self.app.post('/apps/access_token/',
                           data=self.app_dict(),
                           content_type='application/json')
        self.token = json.loads(rv.data.decode('utf-8')).get('token')

    def headers(self, user_token):
        if user_token:
            return {
                'X-APP-ID': 'user_client',
                'X-APP-TOKEN': self.token,
                'X-USER-TOKEN': user_token
            }
        else:
            return {
                'X-APP-ID': 'user_client',
                'X-APP-TOKEN': self.token
            }

    def test_bucketlist(self):
        # get app up and running
        self.create_api_app()
        self.generate_access_token()

        # create a user
        user_token = None

        rv = self.app.post('/users/',
                           headers=self.headers(user_token),
                           data=self.user_dict(),
                           content_type='application/json')
        user_id = json.loads(rv.data.decode('utf-8')).get('user')['id']

        # log in a user
        rv = self.app.post('/users/login',
                           headers=self.headers(user_token),
                           data=self.login_user_dict(),
                           content_type='application/json')
        user_token = json.loads(rv.data.decode('utf-8')).get('token')

        # create a bucketlist item
        rv = self.app.post('/items/',
                           headers=self.headers(user_token),
                           data=self.bucketlist_dict(),
                           content_type='application/json')
        bucketlist_item_id = json.loads(rv.data.decode('utf-8')).get('bucketlist_item')['id']
        assert rv.status_code == 201

        # get a bucketlist item
        rv = self.app.get('/items/' + bucketlist_item_id,
                          headers=self.headers(user_token),
                          content_type='application/json')
        assert rv.status_code == 200

        # edit a user
        new_bucketlist_item = json.dumps(dict(
            name="Star in a Hollywood Blockbuster",
            user_id=user_id,
            modified_on='',
        ))
        rv = self.app.put('/items/' + bucketlist_item_id,
                          headers=self.headers(user_token),
                          data=new_bucketlist_item,
                          content_type='application/json')
        assert rv.status_code == 200
        assert json.loads(rv.data.decode('utf-8')).get('bucketlist_item')['name'] == "Star in a Hollywood Blockbuster"

        # delete a user
        rv = self.app.delete('/items/' + bucketlist_item_id,
                             headers=self.headers(user_token),
                             content_type='application/json')
        assert rv.status_code == 204
        assert Bucketlist.objects.filter(live=False).count() == 1

        # Test Pagination
        # import fixtures
        fixtures(self.db_name, "user", "user/fixtures/users.json")
        fixtures(self.db_name, "bucketlist", "bucketlist/fixtures/bucketlist_items.json")

        # get all users
        rv = self.app.get('/items/',
                          headers=self.headers(user_token),
                          content_type='application/json')
        assert "next" in str(rv.data)

        # get second page of users
        rv = self.app.get('/items/?page=2',
                          headers=self.headers(user_token),
                          content_type='application/json')
        assert "previous" in str(rv.data)
