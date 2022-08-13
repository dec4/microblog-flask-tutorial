from datetime import datetime
from hashlib import md5
from flask_login import UserMixin
from time import time
import jwt
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import app
from app import db
from app import login

"""Define the followers association table.
Note that since this is an auxiliary table using only foreign keys, it is
not necessary to create a Model class.
"""
Followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    following = db.relationship(
        'User', secondary=Followers,
        primaryjoin=(Followers.c.follower_id == id),    # users this_user follows
        secondaryjoin=(Followers.c.followed_id == id),  # users following this_user
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            app.config['SECRET_KEY'],
            algorithm='HS256',
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            id = payload['reset_password']
        except:
            return
        return User.query.get(id)

    def avatar(self, size):
        default_icon_type = 'robohash'
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://gravatar.com/avatar/{digest}?d={default_icon_type}&s={size}'

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(Followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed_posts = Post.query.join(
            Followers, (Followers.c.followed_id == Post.user_id)
        ).filter(
            Followers.c.follower_id == self.id
        )
        own_posts = Post.query.filter_by(user_id=self.id)
        return followed_posts.union(own_posts).order_by(Post.timestamp.desc())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.body}>'
