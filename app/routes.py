from flask import render_template, flash, redirect, url_for, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from app.forms import SignInForm, SignUpForm, ResetPasswordForm
from app import app, db
from app.user import User
import requests
import json

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Authenticate a user
        try:
            # Sign in successful
            user =  User.auth(email, password)
            login_user(user, remember=True)

            flash('User {}, logged in with id={}'.format(
                current_user.email, current_user.get_id())
            )
            return redirect(url_for('index'))
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']

            flash('Error: {}'.format(error))
            return render_template('sign_in.html', title='Sign In', form=form)
        
    return render_template('sign_in.html', title='Sign In', form=form)

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
            user = User.create(name, email, password)
            login_user(user, remember=True)
            flash('User {}, logged in with id={}'.format(
                current_user.email, current_user.get_id())
            )
            return redirect(url_for('index'))
        except requests.exceptions.HTTPError as e:
            print(e)
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']

            flash('Error: {}'.format(error))
            return render_template('sign_up.html', title='Sign Up', form=form)
    else:
        print("form did not validate")
        print(form.errors)
        
    return render_template('sign_up.html', title='Sign Up', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        User.reset(email)
        flash("Password reset email sent")
        
    return redirect(url_for("sign_in"))
    
@app.route('/sign_out', methods=['GET', 'POST'])
@login_required
def sign_out():
    user = current_user
    user.is_authenticated = False
    user.logout()
    logout_user()
    
    return redirect(url_for("index"))

@app.errorhandler(404)
def page_not_found(e):
    flash("Page not found")
    return render_template('404.html'), 404

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("sign_in")), 401
