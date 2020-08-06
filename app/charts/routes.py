from flask import render_template
from flask_login import login_required
from app.charts import bp
import json
import requests
from config import Config

@bp.route('/', methods=['GET'])
@login_required
def dashboard():
    # Run the cloud function
    url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data"
    payload = {
        "access_token": Config.ACCESS_TOKEN,
        "account_id": 123456789,
        "date_range": ["2020-01-01", "2020-01-07"]
        }
    response = requests.get(url, params=payload)
    data = json.loads(response.text)

    spend = sum([float(row['spend']) for row in data])

    return render_template('charts/dashboard.html', title='Dashboard', data=data, spend=spend)