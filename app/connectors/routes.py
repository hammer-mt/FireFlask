from flask import render_template, session, flash, redirect, url_for
from flask_login import login_required, current_user
from app.connectors import bp
from app.teams.models import Team

@bp.route('/', methods=['GET'])
@login_required
def list_connectors():

    if not session.get('team_id'):
        # No team selected
        flash("Please select a team", 'orange')
        return redirect(url_for('teams.list_teams'))
    else:
        team = Team.get(session.get('team_id'))
        print(team.id, current_user.id)

    return render_template('connectors/list_connectors.html', title='Connectors', team=team)

@bp.route('/connections/<platform>')
@login_required
def connect(platform):
    if platform == "facebook":
        token = "test_abc123"
        team = Team.get(session.get('team_id'))
        team.facebook_connect(token)

        print(team.facebook_token)

    return redirect(url_for('connectors.list_connectors'))