from flask import render_template, session, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.connectors import bp
from app.teams.models import Team
from config import Config
import requests
import json

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

@bp.route('/<platform>')
@login_required
def connect(platform):
    if platform == "facebook":
        # Build URI for auth endpoint
        client_param = "?client_id=" + Config.CONNECTORS['facebook_app_id']
        callback_param = '&redirect_uri=' + request.base_url + '/callback'
        state_param = '&state=' + session['csrf_token']
        scope_param = "&scope=ads_read"

        request_uri = Config.CONNECTORS['facebook_authorization_endpoint'] + client_param + callback_param + state_param + scope_param

        return redirect(request_uri)

    flash(f"Error: {platform} not contacted", 'red')
    return redirect(url_for('connectors.list_connectors'))

@bp.route('/<platform>/callback')
@login_required
def callback(platform):
    token = None
    if platform == "facebook":
        # Get authorization code Facebook sent back to you
        code = request.args.get("code")
        print("callback got it: ", code)

        # Construct the token URL
        client_param = "?client_id=" + Config.CONNECTORS['facebook_app_id']
        secret_param = "&client_secret=" + Config.CONNECTORS['facebook_app_secret']
        code_param = '&code=' + code
        callback_param = '&redirect_uri=' + request.base_url

        token_url = Config.CONNECTORS['facebook_token_endpoint'] + client_param + secret_param + callback_param + code_param

        print("trying url: ", token_url)

        # Get the temp token
        temp_token_response = requests.post(token_url)

        # Parse the temp token
        print("temp token dump:", json.dumps(temp_token_response.json()))

        temp_token = temp_token_response.json().get('access_token')

        # Exchange for long lived token
        grant_param = "?grant_type=fb_exchange_token"
        client_param = "&client_id=" + Config.CONNECTORS['facebook_app_id']
        secret_param = "&client_secret=" + Config.CONNECTORS['facebook_app_secret']
        token_param = "&fb_exchange_token=" + temp_token
        
        exchange_url = Config.CONNECTORS['facebook_token_endpoint'] + grant_param + client_param + secret_param + token_param

        # Get the token
        token_response = requests.post(exchange_url)

        # Parse the token
        print("token dump:", json.dumps(token_response.json()))

        token = token_response.json().get('access_token')

        # Save the token
        team = Team.get(session.get('team_id'))
        team.facebook_connect(token)

    if token:
        flash(f"{platform} connected", 'pink')
    else:
        flash(f"Error: {platform} didn't send tokens", 'red')

    return redirect(url_for('connectors.list_connectors'))

@bp.route('/<platform>/disconnect')
@login_required
def disconnect(platform):
    if platform == "facebook":
        team = Team.get(session.get('team_id'))
        team.facebook_connect(None)

    flash(f"{platform} disconnected", 'pink')

    return redirect(url_for('connectors.list_connectors'))