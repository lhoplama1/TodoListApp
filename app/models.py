from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#Items
#Collums:
#item, date, isComplete?, priority, user
#Same kinda format as Post, but change the columns to meet mt TODO needs
class Item(db.Model):
    item = db.Column(db.String(120))
    date = db.Column(db.String(30))
    priority = db.Column(db.Integer)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    inProgress = db.Column(db.Boolean)
    id = db.Column(db.Integer, primary_key=True)



    def __repr__(self):
        return '<Item {}>'.format(self.item)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))