from flask import Flask
from config import Config
import pyrebase
import firebase_admin
from firebase_admin import credentials
from flask_login import LoginManager

login_manager = LoginManager()

firebase = pyrebase.initialize_app(Config.DB)
pyr_db = firebase.database()
pyr_auth = firebase.auth()
pyr_store = firebase.storage()

# Checks for if there is already an active firebase app
if (not len(firebase_admin._apps)):
    cred = credentials.Certificate(Config.DB['serviceAccount'])
    firebase_admin.initialize_app(cred)

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.teams import bp as teams_bp
    app.register_blueprint(teams_bp, url_prefix='/teams')

    return app