from flask import Flask
from config import Config
import pyrebase
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)
app.config.from_object(Config)

firebase = pyrebase.initialize_app(Config.DB)
db = firebase.database()
pyr_auth = firebase.auth()

cred = credentials.Certificate(Config.DB['serviceAccount'])
firebase_admin.initialize_app(cred)

from app import routes