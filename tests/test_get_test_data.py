import pytest
from functions.get_test_data.main import main
from flask import Flask, request
import json

@pytest.fixture()
def func_tester():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.route('/')(lambda: main(request))

    with app.app_context():
        func_tester = app.test_client()
        yield func_tester

def test_get_test_data(func_tester):
    response = func_tester.get('/', query_string=dict(access_token="Mike", account_id="123456789", date_start="2020-01-01", date_end="2020-01-07"))
    assert response.status_code == 200
    test_data = [
        {
            "clicks": "6633.75", 
            "conversions": "804.09", 
            "date": "2020-01-01", 
            "impressions": "2043732.45", 
            "spend": "5360.61"
        }, 
        {
            "clicks": "8884.46", 
            "conversions": "1076.9", 
            "date": "2020-01-02", 
            "impressions": "2737130.16", 
            "spend": "7179.36"
        }, 
        {
            "clicks": "10416.11", 
            "conversions": "1262.56", 
            "date": "2020-01-03", 
            "impressions": "3209004.38", 
            "spend": "8417.06"
        }, 
        {
            "clicks": "11395.85", 
            "conversions": "1381.32", 
            "date": "2020-01-04", 
            "impressions": "3510843.23", 
            "spend": "9208.77"
        }, 
        {
            "clicks": "14497.23", 
            "conversions": "1757.24", 
            "date": "2020-01-05", 
            "impressions": "4466318.22", 
            "spend": "11714.93"
        }, 
        {
            "clicks": "8785.17", 
            "conversions": "1064.87", 
            "date": "2020-01-06", 
            "impressions": "2706542.27", 
            "spend": "7099.13"
        }, 
        {
            "clicks": "14264.91", 
            "conversions": "1729.08", 
            "date": "2020-01-07", 
            "impressions": "4394744.42", 
            "spend": "11527.2"
        }]
    assert json.loads(response.data) == test_data
