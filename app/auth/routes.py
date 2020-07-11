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