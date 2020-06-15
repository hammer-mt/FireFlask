from flask import render_template, flash, redirect, url_for
from app.forms import SignInForm, SignUpForm
from app import app, db, auth
import requests
import json

@app.route('/')
@app.route('/index')
def index():
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
    return render_template('index.html', title='Home', posts=posts)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        #authenticate a user
        try:
            # Sign in successful
            user = auth.sign_in_with_email_and_password(email, password)
            flash('User {}, logged in with token={}'.format(
                email, user['idToken']))
            return redirect(url_for('index'))
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']

            flash('Error: {}'.format(error))
            return render_template('access.html', title='Access', form=form)
        
    return render_template('signin.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        #authenticate a user
        try:
            # Sign up successful
            user = auth.create_user_with_email_and_password(email, password)
            flash('User {}, logged in with token={}'.format(
                email, user['idToken']))
            return redirect(url_for('index'))
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']

            flash('Error: {}'.format(error))
            return render_template('access.html', title='Access', form=form)
        
    return render_template('signup.html', title='Sign Up', form=form)