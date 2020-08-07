from flask import jsonify
import os
import random
from datetime import date, timedelta, datetime

def main(request):
    app_id = os.environ.get('APP_ID')
    app_secret = os.environ.get('APP_SECRET')
    access_token = request.args.get('access_token')

    account_id = request.args.get('account_id')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')

    s_date = datetime.strptime(date_start, '%Y-%m-%d')
    e_date = datetime.strptime(date_end, '%Y-%m-%d')
    delta = e_date - s_date
    
    epoch = datetime(1970,1,1)
    s_since_epoch = (s_date - epoch).days
    e_since_epoch = (e_date - epoch).days
    random.seed(s_since_epoch + e_since_epoch + int(account_id))

    data = []
    for d in range(delta.days + 1):
        date = datetime.strftime(s_date + timedelta(days=d), '%Y-%m-%d')
        shift = random.random() + 0.5
        data.append({
            "date": str(date),
            "spend": str(round(8000.00*shift,2)),
            "clicks": str(round(9900*shift,2)),
            "impressions": str(round(3050000*shift,2)),
            "conversions": str(round(1200*shift,2))
        })

    if app_id and app_secret and access_token:
        return jsonify(data)
    else:
        return None

if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)
    app.route('/')(lambda: main(request))
    app.run(debug=True)

