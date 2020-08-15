from flask import render_template, request, flash, redirect, url_for, session, abort
from flask_login import login_required
from app.charts import bp
import json
import requests
from config import Config
from app.charts.forms import DateForm
from app.teams.models import Team
from datetime import timedelta, datetime

@bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DateForm()
    if form.validate_on_submit():
        start_date = form.start_date.data.strftime('%Y-%m-%d')
        end_date = form.end_date.data.strftime('%Y-%m-%d')
        print(start_date, end_date)
    else:
        yesterday = datetime.today() - timedelta(days=1)
        week_ago = yesterday - timedelta(days=6)

        form.start_date.data = week_ago
        form.end_date.data = yesterday

        start_date = week_ago.strftime('%Y-%m-%d')
        end_date = yesterday.strftime('%Y-%m-%d')

    if not session.get('team_id'):
        # No team selected
        flash("Please select a team", 'orange')
        return redirect(url_for('teams.list_teams'))
    else:
        team = Team.get(session.get('team_id'))
        account_id = team.account_id

        if not account_id:
            # No account id for team
            flash("Please ask account owner to update Account ID", 'orange')
            return redirect(url_for('teams.edit_team', team_id=team.id))
    
    # Run the cloud function
    url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data"
    payload = {
        "access_token": Config.ACCESS_TOKEN,
        "account_id": account_id,
        "date_start": start_date,
        "date_end": end_date
        }
    response = requests.get(url, params=payload)
    data = json.loads(response.text)

    spend = sum([float(row['spend']) for row in data])

    return render_template('charts/dashboard.html', title='Dashboard', data=data, spend=spend, form=form, account_id=account_id)