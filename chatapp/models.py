from chatapp import db, login
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),
                         index=True,
                         unique=True,
                         nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True)
    registered_on = db.Column(db.Date, default=date.today)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar_url(self, size):
        email = self.email or "default@default.com"
        digest = md5(email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_user = db.relationship('User', foreign_keys=from_user_id)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user = db.relationship('User', foreign_keys=to_user_id)
    body = db.Column(db.String(400))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Message {}>".format(self.body)


class Open_chat(db.Model):
    user1_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
    )
    user2_id = db.Column(db.Integer,
                         db.ForeignKey('user.id'),
                         primary_key=True)
    user1 = db.relationship('User', foreign_keys=user1_id)
    user2 = db.relationship('User', foreign_keys=user2_id)
    open_date = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return "<Open_chat {}-{}>".format(self.user1.username,
                                          self.user2.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
