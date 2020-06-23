from flask import Flask
from config import Config
from flask_login import LoginManager
import pyrebase
from user import User

app = Flask(__name__)
app.config.from_object(Config)

firebase = pyrebase.initialize_app(Config.DB)
db = firebase.database()
auth = firebase.auth()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

from app import routes