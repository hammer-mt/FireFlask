from flask import render_template, flash, redirect, url_for, session, escape
from flask_login import current_user, login_required
from app.auth.forms import SignInForm, SignUpForm, ResetPasswordForm, EditProfileForm, UploadPhotoForm, TeamForm, InviteForm
from app.auth import bp
from app import login_manager
from app.auth.models import User, Team, Membership

import requests
import json
from datetime import datetime

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

            if type(e.args[0]) == str:
                 error = e.args[0] # weird bug where not returning json
            else:
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

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data

        #reset password
        try:
            User.reset(email)

            # Reset successful
            flash('Password reset sent for {}. Check your inbox.'.format(
                email), 'teal')
            return redirect(url_for('auth.sign_in'))

        except Exception as e:
            # Reset unsuccessful
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            flash("Error: {}".format(error), 'red')
            
            return render_template('auth/reset_password.html', title='Reset Password', form=form)
        
    return render_template('auth/reset_password.html', title='Reset Password', form=form)

@bp.route('/resend_verification', methods=['GET'])
def resend_verification():
    flash('Sign in again to resend verification email', 'orange')
    
    return redirect(url_for('auth.sign_in'))

@bp.route('/profile', methods=['GET'])
@login_required
def view_profile():
    meta = current_user.get_meta()
    timestamp = current_user.created
    created_date = datetime.fromtimestamp(timestamp / 1000)
    format_date = created_date.strftime("%b %d %Y %H:%M:%S")

    return render_template('auth/view_profile.html',  title='View Profile', meta=meta,
        created_date=format_date)

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        job_title = form.job_title.data

        #edit a user
        try:
            current_user.edit(name, email, job_title)

            # Update successful
            flash('User {}, updated with email={}, name={}, job_title={}'.format(
                 current_user.id, current_user.email, current_user.name, 
                 current_user.get_meta()['job_title']), 'teal')

            return redirect(url_for('auth.view_profile'))

        except Exception as e:
            # Update unsuccessful
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            flash("Error: {}".format(error), 'red')

    form.name.data = current_user.name
    form.email.data = current_user.email

    meta = current_user.get_meta()
    if meta:
        form.job_title.data = meta['job_title']
        
    return render_template('auth/edit_profile.html', title='Edit Profile', form=form)


@bp.route('/profile/upload', methods=['GET', 'POST'])
@login_required
def upload_photo():
    form = UploadPhotoForm()

    if form.validate_on_submit():
        photo = form.photo.data

        #upload an image
        try:
            photo_url = current_user.upload(photo)

            # Update successful
            flash('User {}, updated photo={}'.format(current_user.id, photo_url), 'teal')
            return redirect(url_for('auth.view_profile'))

        except Exception as e:
            # Update unsuccessful
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            flash("Error: {}".format(error), 'red')
        
    return render_template('auth/upload_photo.html', title='Upload Photo', form=form)


@bp.route('/add_team', methods=['GET', 'POST'])
# @login_required
def add_team():
    form = TeamForm()

    if form.validate_on_submit():
        name = form.name.data

        #create a team
        try:
            team = Team.create(name)

            # Update successful
            flash('Team id={}, created with name={}'.format(team.id, team.name), 'teal')
            return redirect(url_for('auth.view_team', team_id=team.id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')
        
    return render_template('auth/add_team.html', title='Add Team', form=form)


@bp.route('/teams/<team_id>', methods=['GET'])
# @login_required
def view_team(team_id):
    team = Team.get(team_id)
    title = 'View Team {}'.format(team.name)
        
    return render_template('auth/view_team.html', title=title, team=team)


@bp.route('/teams/<team_id>/edit', methods=['GET', 'POST'])
# @login_required
def edit_team(team_id):
    form = TeamForm()

    team = Team.get(team_id)

    if form.validate_on_submit():
        name = form.name.data

        #edit a team
        try:
            team.update(name)

            # Update successful
            flash('Team {}, updated with name={}'.format(
                 team.id, team.name), 'teal')

            return redirect(url_for('auth.view_team', team_id=team.id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')

    form.name.data = team.name
        
    return render_template('auth/edit_team.html', title='Edit Team', form=form, 
        team=team)

@bp.route('/teams/<team_id>/add', methods=['GET', 'POST'])
# @login_required
def invite_user(team_id):
    form = InviteForm()

    if form.validate_on_submit():
        email = form.email.data
        role = form.role.data

        #create a team
        try:
            user = User.get_by_email(email)

            if not user:
                user = User.invite(email)
                
            membership = Membership.create(user.id, team_id, role)

            # Update successful
            flash('User {} added to team {} with role {}'.format(membership.user_id, membership.team_id,  membership.role), 'teal')
            return redirect(url_for('auth.view_team', team_id=team_id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')
        
    return render_template('auth/invite_user.html', title='Invite User', form=form)