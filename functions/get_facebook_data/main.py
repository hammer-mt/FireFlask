from flask import jsonify
import os
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights

def main(request):
    access_token = request.args.get('access_token')
    account_id = request.args.get('account_id')

    facebook_app_id = os.environ.get('FACEBOOK_APP_ID')
    facebook_app_secret = os.environ.get('FACEBOOK_APP_SECRET')

    print(access_token, account_id, facebook_app_id, facebook_app_secret)

    # Initialize Facebook App
    FacebookAdsApi.init(facebook_app_id, facebook_app_secret, access_token)

    # Make a call to the Facebook API
    my_account = AdAccount('act_'+account_id)
    fields = ['spend', 'impressions', 'inline_link_clicks', 'actions']
    params = {'level':'account', 'date_preset':'last_30d'}
    insights = my_account.get_insights(fields=fields, params=params)[0]
    data = dict(insights)

    return jsonify(data)

if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)
    app.route('/')(lambda: main(request))
    app.run(debug=True)

