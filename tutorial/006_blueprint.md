### 6: Abstracting user info away in a blueprint

Before we get into the blueprint, let's just fix something that keeps coming up with firebase.

When the server restarts we sometimes get issues where it already has an initialized firebase app. So we now just need to check for it in the __init__.py file.

```
if (not len(firebase_admin._apps)):
    cred = credentials.Certificate(Config.DB['serviceAccount'])
    firebase_admin.initialize_app(cred)
```

Ok now onto the blueprint.

Create a new folder called 'auth' in the app folder. This is where the blueprint will live. Also create one called 'main'.

Do the same in the templates folder.

Move the sign_in and sign_up templates across to the templates/auth folder and the others into templates/main.

Rename the User.py file to models.py.

Now in the app/auth folder add an __init__.py file with these contents
```
from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes
```

You also want to move the routes related to auth into this folder, in a new routes.py file.

```
from flask import render_template, flash, redirect, url_for, session, escape
from flask_login import current_user, login_required
from app.auth.forms import SignInForm, SignUpForm
from app.auth import bp
from app import db, login_manager
from app.models import User

import requests
import json

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@bp.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        #authenticate the user
        try:
            User.auth(email, password)

            # Sign in successful
            flash('User {}, logged in with id={}'.format(
                current_user.email, current_user.id), 'blue')
            return redirect(url_for('main.index'))

        except Exception as e:
            # Sign in unsuccessful
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            flash("Error: {}".format(error), 'red')
            
            return render_template('auth/sign_in.html', title='Sign In', form=form)
        
    return render_template('auth/sign_in.html', title='Sign In', form=form)

@bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        #authenticate a user
        try:
            User.create(name, email, password)

            # Sign up successful
            flash('User {}, created with id={}'.format(
                current_user.email, current_user.id), 'teal')
            return redirect(url_for('main.index'))

        except Exception as e:
            # Sign up unsuccessful
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            flash("Error: {}".format(error), 'red')
        
    return render_template('auth/sign_up.html', title='Sign Up', form=form)
    
@bp.route('/sign_out', methods=['GET', 'POST'])
@login_required
def sign_out():
    user_id = current_user.id # save before user logged out
    User.logout()
    flash("User {} signed out".format(user_id), 'blue')
    return redirect(url_for("main.index"))
```

Notice you have to use the blueprint (@bp) now instead of @app.route.

Also you should move the forms across into auth/forms.py

In main you want to do similar, so here is the main/__init__.py file.
```
from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
```

and here is the new main/routes.py file

```
from flask import render_template, flash, redirect, url_for
from app import login_manager
from app.main import bp


@bp.route('/index')
@bp.route('/')
def index():
    return render_template('main/index.html', title='Home')

@bp.errorhandler(404)
def page_not_found(e):
    flash("Page not found")
    return render_template('main/404.html'), 404

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please sign in to access", 'red')
    return redirect(url_for("auth.sign_in")), 401
```

Now we'll do some refactoring of the way the app/__init__.py file works.

When we're done, it'll use a create_app function now, which is cleaner and sets us up for future testing.
```
from flask import Flask
from config import Config
import pyrebase
import firebase_admin
from firebase_admin import credentials
from flask_login import LoginManager

login_manager = LoginManager()

firebase = pyrebase.initialize_app(Config.DB)
db = firebase.database()
pyr_auth = firebase.auth()

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

    return app

from app import models
```

We also need to change the fireflask.py file to reflect this function.

```
from app import create_app

app = create_app()
```
Last thing to do is to make sure all our routes are updated, including in templates.

So for example 
`{% extends "base.html" %}`
becomes
`{% extends "main/base.html" %}`

and 
`return render_template('index.html', title='Home')`
becomes
`return render_template('main/index.html', title='Home')`

but also 
`return redirect(url_for("sign_in")), 401`
becomes
`return redirect(url_for("auth.sign_in")), 401`

and
`<a href="{{ url_for('sign_out') }}" class="grey-text">Sign Out</a>`
becomes
`<a href="{{ url_for('auth.sign_out') }}" class="grey-text">Sign Out</a>`

just copy these from the github repo or do them manually (I find it easier to just run the flask app and see what errors I get back from it, then adjust to solve that one error)

once you're done, everything should work as normal, but you have a much cleaner and scalable architecture!

