from flask import jsonify
import os

def main(request):
    app_id = os.environ.get('APP_ID')
    app_secret = os.environ.get('APP_SECRET')
    access_token = request.args.get('access_token')

    data = [{
        "date": "2020-01-09",
        "spend": "8000.00",
        "clicks": "9900",
        "impressions": "3050000",
        "conversions": "1200"
    }, {
        "date": "2020-01-10",
        "spend": "8200.00",
        "clicks": "10000",
        "impressions": "3500000",
        "conversions": "1300"
    }, {
        "date": "2020-01-11",
        "spend": "10000.00",
        "clicks": "10900",
        "impressions": "3200000",
        "conversions": "1400"
    }, {
        "date": "2020-01-12",
        "spend": "9000.00",
        "clicks": "12000",
        "impressions": "3700000",
        "conversions": "1000"
    }, {
        "date": "2020-01-13",
        "spend": "7000.00",
        "clicks": "8000",
        "impressions": "3000000",
        "conversions": "800"
    }, {
        "date": "2020-01-14",
        "spend": "8000.00",
        "clicks": "9000",
        "impressions": "3200000",
        "conversions": "1000"
    }, {
        "date": "2020-01-15",
        "spend": "11000.00",
        "clicks": "12000",
        "impressions": "4000000",
        "conversions": "1500"
    }]

    if app_id and app_secret and access_token:
        return jsonify(data)
    else:
        return None

if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)
    app.route('/')(lambda: main(request))
    app.run()

