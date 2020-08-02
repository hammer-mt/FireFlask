from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from app import login_manager
from app.main import bp
import json
import requests
from config import Config


@bp.route('/index')
@bp.route('/')
def index():
    if current_user.is_authenticated:
        
        # Run the cloud function
        url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data"
        payload = {"access_token": Config.ACCESS_TOKEN}
        response = requests.get(url, params=payload)
        data_json = json.loads(response.text)

        return render_template('main/index.html', title='Home', data=data_json)


    return render_template('main/index.html', title='Home')

@bp.errorhandler(404)
def page_not_found(e):
    flash("Page not found")
    return render_template('main/404.html'), 404

@bp.errorhandler(401)
def not_allowed(e):
    flash(str(e))
    return redirect(url_for('index')), 401

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please sign in to access", 'red')
    return redirect(url_for("auth.sign_in")), 401
