from flask import Flask
from config import Config, config_db

app = Flask(__name__)
app.config.from_object(Config)

import pyrebase

firebase = pyrebase.initialize_app(config_db)
db = firebase.database()
auth = firebase.auth()

from app import routes