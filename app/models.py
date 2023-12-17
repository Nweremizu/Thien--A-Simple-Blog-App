from app import app
from app import db, login
from time import time
import jwt
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# The Auxilary Table for the followers
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(230))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # followers transerval function
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_followers(self):
        """
        Gets the Number of users that are following a User
        :return:
        """
        return self.followers.count()

    def get_followed(self) -> int:
        """
        Gets the Number of Users the User is Following
        :return:
        """
        return self.followed.count()

    def get_posts_count(self) -> int:
        """
        Gets The Number Of Posts Of A User
        :return:
        """
        return self.posts.count()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_data = db.Column(db.LargeBinary)
    image_url = db.Column(db.String(100),
                          default='http://www.palmares.lemondeduchiffre.fr/images/joomlart/demo/default.jpg')
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tag = db.relationship('Tag', back_populates='posts')

    def __repr__(self):
        return f'<Post {self.body}>'

    def get_tags(self):
        return self.tags.split(',')

    def fetch_author(self):
        user = User.query.filter_by(id=self.user_id).first()
        return user

    def get_author(self):
        user = User.query.filter_by(id=self.user_id).first()
        username = user.username.capitalize()
        return username

    def author_avatar(self):
        user = User.query.filter_by(id=self.user_id).first()
        return user.avatar(128)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    posts = db.relationship('Post', back_populates='tag')

    def __repr__(self):
        return f'<Tag {self.name}>'

    def get_posts(self):
        return self.posts.all()