import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_DB = os.environ.get('MONGO_DB') or 'mongodb://localhost:27017/fplayux'