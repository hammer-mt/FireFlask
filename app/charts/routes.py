from flask import render_template
from app.charts import bp
import json
import requests
from config import Config

@bp.route('/', methods=['GET'])
def dashboard():
    # Run the cloud function
    url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data"
    payload = {"access_token": Config.ACCESS_TOKEN}
    response = requests.get(url, params=payload)
    data_json = json.loads(response.text)

    text = [row['date'] for row in data_json]
    values = [row['spend'] for row in data_json]

    return render_template('charts/dashboard.html', title='Dashboard', data=data_json, text=text, values=values)