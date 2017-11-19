from application import db
from user.models import User


class Bucketlist(db.Document):
    external_id = db.StringField(db_field="ei")
    name = db.StringField(db_field="n")
    user = db.ReferenceField(User, db_field="u")
    created_on = db.DateTimeField(db_field="cr")
    modified_on = db.DateTimeField(db_field="mo")
    live = db.BooleanField(db_field="l", default=True)

    meta = {
        'indexes': [('external_id', 'live'), ('user', 'live')]
    }
