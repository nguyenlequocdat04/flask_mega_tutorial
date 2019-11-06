from pymodm.errors import DoesNotExist
from model.user import UserDAO
from werkzeug.security import check_password_hash

class UserService(object):
    @staticmethod
    def get_by_username(username):
        try:
            return UserDAO.get_by_username(username)
        except DoesNotExist:
            return None

    @staticmethod
    def login(username, password):
        try:
            user = UserDAO.get_by_username(username)
            if check_password_hash(user.password, password):
                return user
            else:
                return None
        except DoesNotExist:
            return None

    @staticmethod
    def get_all():
        try:
            return UserDAO.get_all()
        except DoesNotExist:
            return None

    @staticmethod
    def create_user(username, password, email):
        try:
            return UserDAO.create_user(username, password, email)
        except:
            return None
