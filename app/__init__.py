from flask import Flask
from config import Config
import pyrebase

app = Flask(__name__)
app.config.from_object(Config)

firebase = pyrebase.initialize_app(Config.DB)
db = firebase.database()
auth = firebase.auth()

from app import routes