from flask import render_template, flash, redirect, url_for, session, escape, abort
from flask_login import current_user, login_required
from app.teams.forms import TeamForm, InviteForm
from app.teams import bp
from app.auth.models import User
from app.teams.models import Team, Membership

import requests
import json
from datetime import datetime

@bp.route('/add_team', methods=['GET', 'POST'])
@login_required
def add_team():
    form = TeamForm()

    if form.validate_on_submit():
        name = form.name.data

        #create a team
        try:
            team = Team.create(name)

            Membership.create(current_user.id, team.id, "OWNER")

            # Update successful
            flash('Team id={}, created with name={}'.format(team.id, team.name), 'teal')
            return redirect(url_for('teams.view_team', team_id=team.id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')
        
    return render_template('teams/add_team.html', title='Add Team', form=form)


@bp.route('/<team_id>', methods=['GET'])
@login_required
def view_team(team_id):
    team = Team.get(team_id)
    users_by_team = Membership.get_users_by_team(team_id)

    team_members = []
    authorized = False
    role = False
    for membership in users_by_team:
        membership_data = membership.val()
        user = User.get(membership_data['user_id'])

        member = {
            "id": user.id,
            "name": user.name,
            "role": membership_data['role'],
            "membership_id": membership.key()
        }
        team_members.append(member)

        if current_user.id == user.id:
            authorized = True
            role = membership_data['role']

    if not authorized:
        abort(401, "You don't have access to that team")

    session["team_id"] = team.id
    session["team_name"] = team.name

    title = 'View Team {}'.format(team.name)
        
    return render_template('teams/view_team.html', title=title, team=team, team_members=team_members, role=role)


@bp.route('/<team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):

    role = Membership.user_role(current_user.id, team_id)
    if role not in ["ADMIN", "OWNER"]:
        abort(401, "You don't have access to edit this team.")

    form = TeamForm()

    team = Team.get(team_id)

    if form.validate_on_submit():
        name = form.name.data
        account_id = form.account_id.data
        conversion_event = form.conversion_event.data

        #edit a team
        try:
            team.update(name, account_id, conversion_event)

            # Update successful
            flash('Team {}, updated with name={}'.format(
                 team.id, team.name), 'teal')

            return redirect(url_for('teams.view_team', team_id=team.id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')

    form.name.data = team.name
    form.account_id.data = team.account_id
    form.conversion_event.data = team.conversion_event
        
    return render_template('teams/edit_team.html', title='Edit Team', form=form, 
        team=team)

@bp.route('/<team_id>/invite', methods=['GET', 'POST'])
@login_required
def invite_user(team_id):
    role = Membership.user_role(current_user.id, team_id)
    if role not in ["ADMIN", "OWNER"]:
        abort(401, "You don't have access to invite to this team.")

    form = InviteForm()

    team = Team.get(team_id)

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
            return redirect(url_for('teams.view_team', team_id=team.id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')
        
    return render_template('teams/invite_user.html', title='Invite User', form=form, team=team)

@bp.route('/', methods=['GET'])
@login_required
def list_teams():
    teams_by_user = Membership.get_teams_by_user(current_user.id)

    teams_list = []
    for membership in teams_by_user:
        membership_data = membership.val()
        team_data = Team.get(membership_data['team_id'])

        team = {
            "id": team_data.id,
            "name": team_data.name,
            "role": membership_data['role'],
        }
        teams_list.append(team)

    return render_template('teams/list_teams.html', title='Teams', teams_list=teams_list)

@bp.route('/<membership_id>/delete', methods=['GET', 'POST'])
@login_required
def remove_user(membership_id):

    membership = Membership.get(membership_id)

    role = Membership.user_role(current_user.id, membership.team_id)
    if role not in ["ADMIN", "OWNER"]:
        abort(401, "You don't have access to remove this user.")
    elif membership.role == "OWNER":
        abort(401, "You cannot remove the owner of the account.")
    else:
        membership.remove()

        flash('User {} removed from team {}'.format(membership.user_id, membership.team_id), 'teal')
        return redirect(url_for('teams.view_team', team_id=membership.team_id))
