from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from web import db, login_manager, app
from flask_login import UserMixin
import flask_whooshalchemy as wa
import json
from time import time


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):

    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True)
    joined_day = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
wa.whoosh_index(app,User)






class Messages(db.Model):

    __searchable__ = ['subjects','messages']
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    emails = db.Column(db.Text, nullable=False)
    subjects = db.Column(db.Text)
    messages = db.Column(db.Text, nullable=False)



    def __repr__(self):
        return f"Messages('{self.subjects}', '{self.date_posted}', '{self.messages}')"

wa.whoosh_index(app,Messages)



class Phonecall(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    emails = db.Column(db.Text, nullable=False)
    phones = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f"Phonecall('{self.names}', '{self.date_posted}', '{self.phones}')"



class Emails(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    emails = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Emails('{self.emails}')"
