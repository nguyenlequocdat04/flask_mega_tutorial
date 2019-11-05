from pymodm.errors import DoesNotExist
from model.user import UserDAO
from werkzeug.security import check_password_hash

class UserService(object):
    @staticmethod
    def login(username, password):
        try:
            user = UserDAO.login(username)
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
