from pymodm import fields, MongoModel
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, MongoModel):
    username = fields.CharField(primary_key=True)
    password = fields.CharField()
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

class UserDAO(object):
    @staticmethod
    def get_all():
        return User.objects.values().all()

    @staticmethod
    def get_by_username(username):
        return User.objects.get({'_id': username})

    @staticmethod
    def create_user(username, password):
        User(username=username, password=generate_password_hash(password)).save()

@login.user_loader
def get_user(username):
    return User.objects.get({'_id': username})