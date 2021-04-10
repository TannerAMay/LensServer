from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))

    def get_id(self):
        return self.username