from flask_user import UserMixin
from app import db

class User(db.Document, UserMixin):
    # User authentication information
    username = db.StringField(default='')
    password = db.StringField()
