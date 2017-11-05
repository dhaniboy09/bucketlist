from application import db


class App(db.Document):
    """ Creates a Model for the apps accessing
        the API
    """
    app_id = db.StringField(db_field="ai", unique=True)
    app_secret = db.StringField(db_field="as")

    meta = {
        'indexes': [('app_id')]
    }


class Access(db.Document):
    """ Model for storing the token generated for the Apps accessing the API

        app is foreign_key referencing app_id in the APP model
    """
    app = db.ReferenceField(App, db_field="a")
    token = db.StringField(db_field="t")
    expires = db.DateTimeField(db_field="e")
