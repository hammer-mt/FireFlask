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

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='Home')

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
