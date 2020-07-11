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
