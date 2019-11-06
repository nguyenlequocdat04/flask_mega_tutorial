from pymodm import fields, MongoModel
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
import datetime


class User(UserMixin, MongoModel):
    username = fields.CharField(primary_key=True)
    email = fields.CharField()
    password = fields.CharField()
    about_me = fields.CharField(max_length=140)
    last_seen = fields.DateTimeField(default=datetime.datetime.now())
    # def is_active(self):
    #     # Here you should write whatever the code is
    #     # that checks the database if your user is active
    #     return self.active

    # def is_anonymous(self):
    #     return False

    # def is_authenticated(self):
    #     return True

    class Meta:
        final = True
        collection_name = 'users'

    def get_id(self):
        return self.username
        pass

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class UserDAO(object):
    @staticmethod
    def get_all():
        return User.objects.values().all()

    @staticmethod
    def get_by_username(username):
        return User.objects.get({'_id': username})

    @staticmethod
    def create_user(username, password, email):
        return User(username=username, password=generate_password_hash(
            password), email=email).save()


@login.user_loader
def get_user(username):
    return User.objects.get({'_id': username})
