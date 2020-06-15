import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

config_db = {
    "apiKey": os.environ.get('FIREBASE_API_KEY'),
    "authDomain": "fireflask-ef97c.firebaseapp.com",
    "databaseURL": "https://fireflask-ef97c.firebaseio.com",
    "projectId": "fireflask-ef97c",
    "storageBucket": "fireflask-ef97c.appspot.com",
    "messagingSenderId": "381149552037",
    "appId": "1:381149552037:web:47b684b770d91d396e9c4c",
    "measurementId": "G-H6VEF5PZJP"
}