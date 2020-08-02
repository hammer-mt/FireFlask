### 4: Set up authentication

Set up your new branch
`git checkout -b "branch"`

We're going to connect with firebase in this part, and use it to authenticate a user, then let them save and retrieve data from the NoSQL database.

Note we're adapting this from a SQL based tutorial for a NoSQL database, so we need to make a few changes. 

Let's first map out the things we need to do:

1. Set any environment variables in the .flaskenv file
2. Set the right path and other variables in the config.py file
3. Initialize the database in the __init__.py file 
4. Set up the models.py file to create the user class
5. Set up Flask-Login functionality and connect to form and routes
6. Flash user onto html page when logged in

We have to piece this together through several tutorials and just looking at the documentation, because I couldn't see any one place that had what we need. Most of the firebase flask tutorials don't integrate with flask-login (so sessions aren't persisted) and most of the flask-login tutorials are with SQLAlchemy.

- [Flask and Firebase and Pyrebase Oh My](https://blog.upperlinecode.com/flask-and-firebase-and-pyrebase-oh-my-f30548d68ea9)
- [Heating up with firebase tutorial on how to integrate firebase into your app](https://blog.devcolor.org/heating-up-with-firebase-tutorial-on-how-to-integrate-firebase-into-your-app-6ce97440175d)
- [Using Flask-Login for User Management with Flask](https://realpython.com/using-flask-login-for-user-management-with-flask/)
- [Firebase Authentication with Python including Flask API](https://www.youtube.com/watch?v=FCw5PFDb99k)
- [Manage Session Cookies](https://firebase.google.com/docs/auth/admin/manage-cookies#python)


Example models.py file
```
from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body) 
```

Now we're finished with the spec, let's commit our tutorial page and push to the remote branch.

Check you're on the right branch
`git branch`

Make sure you're up to date with your commits
`git status`
`git add .`
`git commit -m "added spec for auth to the tutorial"`

Push the branch changes upstream to github
`git push --set-upstream origin auth`

Once you've done this for a branch you can just do
`git push`

And it'll work next time without the extra set upstream stuff

This next part will be a little messy because I couldn't find one tutorial that did what I needed. Will need to piece a few things together.

First let's go to firebase: [firebase.google.com](https://firebase.google.com/) and create a new project.

Go to database and create a new database, start it in test mode.

Make sure your virtual environment is active.

`venv\Scripts\activate`

Now let's install pyrebase and update our requirements.txt

`pip install pyrebase4`
`pip install firebase_admin`
`pip freeze > requirements.txt`

Note you might run into a weird issue with one of the libraries.

Go to venv > Lib > site-packages > crypto

If it's lower case, change the folder name to Crypto (capitalize the C), and it should work.

Add this to the routes file
`import pyrebase`

Go to the firebase project overview and click the < /> symbol, register the app and get the config code.

Change your config file to add the DB variable (note it needs to be capitalized)
```
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)

    DB = {
        "apiKey": os.environ.get('FIREBASE_API_KEY'),
        "authDomain": "fireflask-ef97c.firebaseapp.com",
        "databaseURL": "https://fireflask-ef97c.firebaseio.com",
        "projectId": "fireflask-ef97c",
        "storageBucket": "fireflask-ef97c.appspot.com",
        "messagingSenderId": "381149552037",
        "appId": "1:381149552037:web:47b684b770d91d396e9c4c",
        "measurementId": "G-H6VEF5PZJP",
        "serviceAccount": "app/firebase-private-key.json"
    }
```

Add your firebase api key to the .flaskenv file
`FIREBASE_API_KEY=abcdefghijklmnopqrstuvwxyz12345679`

Go to settings -> Service Accounts and then generate a new private key. 

That will download a JSON file that you can connect to your config variables. Rename it to `firebase-private-key.json` then save it it to the app folder.

Add that file to the .gitignore so that it doesn't get tracked by git and uploaded to github.
```
# Service account
firebase-private-key.json
```

Change your __init__.py file to this
```
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
```

Now you have initialized both Pyrebase and Firebase Admin. You need both because Firebase Admin gives you the ability to look up users by their user id, and Pyrebase makes logging in easier.

Ok now let's build the ability to log in.

Make sure at the top of the routes file you pull in the following.

```
from flask import render_template, flash, redirect, url_for, session
from flask_login import LoginManager, current_user, login_required
from app.forms import SignInForm, SignUpForm
from app import app, db
from app.user import User
import requests
import json

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
```

The login manager code is a requirement of flask to persist user sessions.

In the routes.py we need to change the login to this:
```
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        #authenticate a user
        try:
            # Sign in successful
            User.auth(email, password)
            flash('User {}, logged in with id={}'.format(
                current_user.email, current_user.id)
            )
            return redirect(url_for('index'))

        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
            return render_template('sign_in.html', title='Sign In', form=form)
        
    return render_template('sign_in.html', title='Sign In', form=form)

```

The signup part of routes should look like this:

```
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        #authenticate a user
        try:
            # Sign up successful
            User.create(name, email, password)
            flash('User {}, created with id={}'.format(
                current_user.email, current_user.id)
            )
            return redirect(url_for('index'))

        except Exception as e:
            flash('Error: {}'.format(e), 'danger')
            return render_template('sign_up.html', title='Sign Up', form=form)
        
    return render_template('sign_up.html', title='Sign Up', form=form)
```

It's worth adding these routes too:
```
@app.route('/sign_out', methods=['GET', 'POST'])
@login_required
def sign_out():
    User.logout()
    return redirect(url_for("index"))

@app.errorhandler(404)
def page_not_found(e):
    flash("Page not found")
    return render_template('404.html'), 404

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("sign_in")), 401
```

For the forms.py we have to change it to this:
```
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=255, 
        message="Password must be 6+ characters")])
    submit = SubmitField('SIGN UP')

class SignInForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('SIGN IN')
```

You might need at this point to install email_validator and flask login
`pip install email_validator`
`pip install flask-login`

Remember to update your requirements.txt
`pip freeze > requirements.txt`

Now we update the user model at user.py:

```
from flask_login import UserMixin
from app import pyr_auth
from firebase_admin import auth
from flask_login import login_user, logout_user

class User(UserMixin):
    def __init__(self, uid, email, name):
        self.id = uid
        self.email = email
        self.name = name
    
    @staticmethod
    def get(user_id):
        try:
            firebase_user = auth.get_user(user_id)
            print('Successfully fetched user data: {0}'.format(firebase_user.uid))

            flask_user = User(
                uid=firebase_user.uid,
                email=firebase_user.email,
                name=firebase_user.display_name
            )
            return flask_user
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def create(name, email, password):
        firebase_user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )
        print('Sucessfully created new user: {0}'.format(firebase_user.uid))

        flask_user = User(
            uid=firebase_user.uid,
            email=firebase_user.email,
            name=firebase_user.display_name
        )
        login_user(flask_user, remember=True)
        return flask_user

    @staticmethod
    def auth(email, password):
        pyr_user = pyr_auth.sign_in_with_email_and_password(email, password)
        print(pyr_user)
        flask_user = User(
            uid=pyr_user['localId'],
            email=pyr_user['email'],
            name=pyr_user['displayName']
        )
        login_user(flask_user, remember=True)
        return flask_user

    @staticmethod
    def logout():
        logout_user()
```


Finally change the sign_in.html to this:

```
{% extends "base.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.email.label }}<br>
            {{ form.email(size=32) }}<br>
            {% for error in form.email.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}<br>
            {% for error in form.password.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

the sign_up.html to this:

```
{% extends "base.html" %}

{% block content %}
    <h1>Sign Up</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.name.label }}<br>
            {{ form.name(size=32) }}<br>
            {% for error in form.name.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>
            {{ form.email.label }}<br>
            {{ form.email(size=32) }}<br>
            {% for error in form.email.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}<br>
            {% for error in form.password.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}

```

I've also updated the index:

```
{% extends "base.html" %}

{% block content %}
    {% if current_user.is_authenticated %}
    <h1>Hi, {{ current_user.name }}!</h1>
    {% else %}
    <h1>Hi, come here often?</h1>
    {% endif %}
{% endblock %}
```

And the base

```
<html>
    <head>
        {% if title %}
        <title>{{ title }} - FireFlask</title>
        {% else %}
        <title>FireFlask</title>
        {% endif %}
    </head>
    <body>
        <div>
            FireFlask:
            <a href="{{ url_for('index') }}">Home</a>
            {% if current_user.is_authenticated %}
            <a href="{{ url_for('sign_out') }}">Sign Out</a>
            {% else %}
            <a href="{{ url_for('sign_up') }}">Sign Up</a>
            <a href="{{ url_for('sign_in') }}">Sign In</a>
            {% endif %}
        </div>
        <hr>
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        {% for category, message in messages %}
        <div class="alert alert-{{ category }} alert-dismissible" role="alert">
            <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            {{ message }}
        </div>
        {% endfor %}
        {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
        <hr>
        <footer>
            {% if current_user.is_authenticated %}
            <p>Current user: {{ current_user.id }}</p>
            {% else %}
            <p>Current user: Anonymous</p>
            {% endif %}
        </footer>
    </body>
</html>
```

This makes it easier to debug and check it's working.

Ok that's a lot of code, let's review what it does.

We created a User object that controls how each user is authenticated.

This has some requirements from flask, like the user loader function, and communicates to firebase for us.

We talk to firebase in two ways - firebase admin and pyrebase.

Unfortunately these two libraries are both needed as pyrebase does signin really well, and firebase admin does creation of users better (you can pass a display name) and lets you look up users by universal id (uid).

This last part is really important, because pyrebase only allows you to look up users with a token, which will expire after an hour.

We're bypassing firebases token system all together and using flasks, because this system is simple and we don't want users being logged out all the time.

This implementation means that we don't store any sensitive info about users on our servers, it's all handled by firebase, including the tokens. 

