from pymodm import fields, MongoModel
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, MongoModel):
    username = fields.CharField(primary_key=True)
    password = fields.CharField()
    class Meta:
        final = True
        collection_name = 'users'

    def get_id(self):
        return self.username
        pass

class UserDAO(object):
    @staticmethod
    def get_all():
        return User.objects.values().all()

    @staticmethod
    def login(username):
        return User.objects.get({'_id': username})

    @staticmethod
    def create_sample_user(username, password):
        User(username=username, password=generate_password_hash(password)).save()

@login.user_loader
def get_user(username):
    User.objects.get({'_id': username})