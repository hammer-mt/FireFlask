from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app import app
import pyrebase
import os

config = {
    "apiKey": os.environ['FIREBASE_API_KEY'],
    "authDomain": "fireflask-ef97c.firebaseapp.com",
    "databaseURL": "https://fireflask-ef97c.firebaseio.com",
    "projectId": "fireflask-ef97c",
    "storageBucket": "fireflask-ef97c.appspot.com",
    "messagingSenderId": "381149552037",
    "appId": "1:381149552037:web:47b684b770d91d396e9c4c",
    "measurementId": "G-H6VEF5PZJP"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Michael'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)