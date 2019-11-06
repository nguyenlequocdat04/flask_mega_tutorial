from flask import Flask
from config import Config
from pymodm import connect
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
connect(app.config['MONGO_DB'])
login = LoginManager(app)
login.login_view = 'login'
from app import routes