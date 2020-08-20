from flask import jsonify
import os
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights

def main(request):
    access_token = request.args.get('access_token')
    account_id = request.args.get('account_id')

    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')

    conversion_event = request.args.get('conversion_event')

    facebook_app_id = os.environ.get('FACEBOOK_APP_ID')
    facebook_app_secret = os.environ.get('FACEBOOK_APP_SECRET')

    print(access_token, account_id, facebook_app_id, facebook_app_secret)

    # Initialize Facebook App
    FacebookAdsApi.init(facebook_app_id, facebook_app_secret, access_token)

    # Make a call to the Facebook API
    my_account = AdAccount('act_'+account_id)
    fields = ['spend', 'impressions', 'inline_link_clicks', 'actions']
    params = {
        'level': 'account', 
        'time_range': {'since': date_start, 'until': date_end}, 
        'time_increment': 1
        }
    
    insights = my_account.get_insights(fields=fields, params=params)
    data = []
    for day in insights:
        format_data = {}
        format_data['date'] = day['date_start']
        format_data['impressions'] = day['impressions']
        format_data['clicks'] = day['inline_link_clicks']
        format_data['spend'] = day['spend']

        # Pull out conversion metric
        conversions = [action.get('value') for action in day['actions'] if action.get('action_type') == conversion_event]
        
        if conversions:
            format_data['conversions'] = conversions[0]
        else:
            format_data['conversions'] = "0"
        
        # Append to the data list
        data.append(format_data)

    return jsonify(data)

if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)
    app.route('/')(lambda: main(request))
    app.run(debug=True)

