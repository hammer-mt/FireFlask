### 12: Connecting a User's Facebook account

Now for a big leap in our applications usefulness - connecting to an external API via oauth. We'll use the Facebook API for this, and it will involve letting a user authenticate via Facebook, then passing that token to a cloud function, which we'll modify from the test one we made to actually pull data from facebook. 

- [https://realpython.com/flask-google-login/](https://realpython.com/flask-google-login/)
- [https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask](https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask)
- [https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow](https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow)

Because we plan to add multiple connectors, to keep our code clean, we're going to abstract away connectors into its own blueprint. So let's run through that setup process first.

The process to create a blueprint again is:
- Create a 'connectors' folder in app
- Create a 'connectors' folder in app/templates
- Create an __init__.py file in app/connectors
- Create a routes.py file in app/connectors
- Register the blueprint in app/__init__.py
- Create a list_connectors.html file in templates/connectors

Contents of the __init__.py file:
```
from flask import Blueprint

bp = Blueprint('connectors', __name__)

from app.connectors import routes
```

Contents of the routes.py file:
```
from flask import render_template
from flask_login import login_required
from app.connectors import bp

@bp.route('/', methods=['GET', 'POST'])
@login_required
def list_connectors():
    return render_template('connectors/list_connectors.html', title='Connectors')

```


Here's how you register the blueprint in app/__init__.py in the create_app function
```
from app.connectors import bp as connectors_bp
app.register_blueprint(connectors_bp, url_prefix='/connectors')
```

Finally here's the contents of list_connnectors.html:
```
{% extends "main/base.html" %}

{% block content %}
<h3>Teams</h3>

<div class="row">
    <div class="col s6">
        <p>A list of all of the connectors to platform integrations.</p>
    </div>

</div>
<br>


<div class="row">
    <div class="col s3">
        <a href="#">
            <div class="card">
                <div class="card-content center-align team">
                    <span class="card-title">Facebook Ads</span>
                </div>
                <div class="card-action">
                    <p class="center-align">
                        <button type="submit" name="btn" class="waves-effect waves-light btn blue">
                        CONNECT
                        </button>
                    </p>
                </div>
            </div>
        </a>

    </div>
</div>

{% endblock %}

```

Let's also provide a link to connectors in the navbar in templates/main/_nav.html
`<li id="connectors-list_connectors"><a href="{{ url_for('connectors.list_connectors') }}">Connectors</a></li>`

Or we can visit http://127.0.0.1:5000/connectors

The way we want connectors to work is as follows:

- the connections page won't be visible for anyone who's not the owner of the account
- if an owner visits the connectors page without a team selected, it prompts them to choose a team
- when on the team page, there will be a link to connectors, and the link in the navbar will work
- visiting the connectors page will list all connectors for that owner and team
- there will be one connector per platform (in this case for now just Facebook Ads)
- if the connector isn't connected, you have to option to connect, if it is, you can reconnect
- clicking connect will take you through the oauth process to get and store a token
- reconnect will do the same, except the old token that was stored will be replaced
- the token will be stored in the database under team, but not visible in the team page

First step, let's borrow the logic we used in charts to redirect the user if they haven't selected a team.

Add this to the imports in connectors/routes.py:
```
from flask import render_template, session, flash, redirect, url_for
from flask_login import login_required, current_user
from app.connectors import bp
from app.teams.models import Team
```

Then add this to the list_connectors function:
```
if not session.get('team_id'):
        # No team selected
        flash("Please select a team", 'orange')
        return redirect(url_for('teams.list_teams'))
    else:
        team = Team.get(session.get('team_id'))
        print(team.id, current_user.id)
```

We want to add links to the connectors for a team, as well as back again.

In the templates/connectors/list_connectors.html, add this:
```
<div class="col s6 m4">
    <a href="{{ url_for('teams.view_team', team_id=team.id) }}">< Back to Team page</a>
</div>
```

Then make sure you change the render template to pass the team to the page:

`return render_template('connectors/list_connectors.html', title='Connectors', team=team)`

We can also add a link from the view team page, above the table in the card:
```
<p>
    <a href="{{ url_for('connectors.list_connectors') }}">
        <button type="submit" name="btn" class="waves-effect waves-light btn pink">
            CONNECTORS
        </button>
    </a>
</p>
```

Let's also add a little facebook logo as well, to make it look more official. We want to use font-awesome for this, so let's install it in the header in base.html

```
<!-- Font Awesome Icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
```

Now just add this line underneath the facebook connector span.
`<i class="fa fa-facebook-f fa-5x"></i>`

You need to add some css in the main css file.
```
.connector {
    height: 12em;
    overflow: hidden;
}
.connector-title {
    margin-bottom: 1em !important;
}
```

Then add these properties so it works.

```
<div class="row">
    <div class="col s12 m6 l4">
        <a href="#">
            <div class="card">
                <div class="card-content center-align connector">
                    <span class="card-title connector-title">Facebook Ads</span>
                    <i class="fa fa-facebook-f fa-5x"></i>
                </div>
                <div class="card-action">
                    <p class="center-align">
                        <button type="submit" name="btn" class="waves-effect waves-light btn pink">
                        CONNECT
                        </button>
                    </p>
                </div>
            </div>
        </a>

    </div>
</div>
```

Do a hard refresh, CTRL + F5 to reload.

Now let's do the oauth handshake routing. For this we'll need to do a lot of configuration so that when we ping facebook they come back with a form that the user can login and authorize, which then we can get the tokens.

First we need to make a new Facebook app by visiting here: https://developers.facebook.com/apps/

Click to add new app and choose business integrations.

Give it a name, contact email and select if you're just using it for yourself or for others. You can also choose to connect it to a business manager.

Copy the app ID (should be at the top of the page) and the app secret (in settings > basic). While you're there, add to the App Domains:
`http://127.0.0.1:5000/`
and
`https://fireflask-ef97c.uc.r.appspot.com/`

Add the following to your config.py class

```
CONNECTORS = {
    "facebook_app_id": "2380723265555589",
    "facebook_app_secret": os.environ.get('FACEBOOK_APP_SECRET'),
    "facebook_authorization_endpoint": "https://www.facebook.com/v6.0/dialog/oauth",
    "facebook_token_endpoint": "https://graph.facebook.com/v6.0/oauth/access_token"
}
```

Then in your flaskenv file add the facebook app secret:
`FACEBOOK_APP_SECRET=abcdefghijklmnopqrstuvwxyz`

also in your env.yaml.
`FACEBOOK_APP_SECRET: abcdefghijklmnopqrstuvwxyz`

Great, now let's add the routes we need to connectors.

First let's just simply pass the name of the platform across to our route.

In list_connectors the card in an a tag with this href:
`<a href="{{ url_for('connectors.connect', platform='facebook') }}">`

Then in routes we need this:
```
@bp.route('/<platform>')
@login_required
def connect(platform):
    print(platform)
    return redirect(url_for('connectors.list_connectors'))
```

You should see it returns you back to the connectors page and prints out facebook to the console.

Ok now let's hardcode a token (pretend facebook is sending one back) and figure out our adjustment to teams.

First modify the init method for Team:

```
def __init__(self, id_, name, account_id, facebook_token=None):
    self.id = id_
    self.name = name
    self.account_id = account_id
    self.facebook_token = facebook_token
```
Note we pass None as the default, so we don't need to modify all our other code around creating teams.

Then the get method:
```
@staticmethod
def get(team_id):
    team_data = pyr_db.child('teams').child(team_id).get().val()
    team = Team(
        id_=team_id, 
        name=team_data['name'],
        account_id=team_data.get('account_id'),
        facebook_token=team_data.get('facebook_token')
    )
    return team
```

So then we want a new method to just save the facebook token.

```
def facebook_connect(self, token):
    pyr_db.child('teams').child(self.id).update({
        "facebook_token": token,
    })

    self.facebook_token = token
```

Now we should be able to modify the route to save the token and print a test token.

```
@bp.route('/<platform>')
@login_required
def connect(platform):
    if platform == "facebook":
        token = "test_abc123"
        team = Team.get(session.get('team_id'))
        team.facebook_connect(token)

        print(team.facebook_token)

    return redirect(url_for('connectors.list_connectors'))
```

Now if you run this it should print the token, and save it to the realtime database in firebase.

Lets also change the state of the button when it is connected, and provide a way to sever the connection.

```
 <div class="card">
    <div class="card-content center-align connector">
        <span class="card-title connector-title">Facebook Ads</span>
        <i class="fa fa-facebook-f fa-5x blue-text"></i>
    </div>
    <div class="card-action">
        <p class="center-align">
            {% if team.facebook_token %}
            <button type="submit" name="btn" class="waves-effect waves-light btn pink disabled">
                CONNECTED
            </button>
            {% else %}
            <a href="{{ url_for('connectors.connect', platform='facebook') }}">
                <button type="submit" name="btn" class="waves-effect waves-light btn pink">CONNECT</button>
            </a>
            {% endif %}
        </p>
    </div>
</div>
```

This should make the button go gray when the facebook token is available.

Now let's make a route where they could disconnect.

```
@bp.route('/<platform>/disconnect')
@login_required
def disconnect(platform):
    if platform == "facebook":
        team = Team.get(session.get('team_id'))
        team.facebook_connect(None)

    return redirect(url_for('connectors.list_connectors'))
```

This just passes none instead of the token, wiping it out.

Then lets modify the template again to allow this behavior. 
```
<div class="card">
    <div class="card-content center-align connector">
        <span class="card-title connector-title">Facebook Ads</span>
        <i class="fa fa-facebook-f fa-5x blue-text"></i>
    </div>
    <div class="card-action">
        {% if team.facebook_token %}
        <div class="row center-align">
            <button type="submit" name="btn" class="waves-effect waves-light btn pink disabled">
                CONNECTED
            </button>
        </div>
        
        <a href="{{ url_for('connectors.disconnect', platform='facebook') }}">
            <div class="row center-align disconnect">
                Disconnect <i class="tiny material-icons inline-icon">close</i>
            </div>
        </a>
        
        {% else %}
        <a href="{{ url_for('connectors.connect', platform='facebook') }}">
            <div class="row center-align">
                <button type="submit" name="btn" class="waves-effect waves-light btn pink">CONNECT</button>
            </div>
        </a>
        
        {% endif %}
    </div>
</div>
```

Now there's a link underneath the button that says diconnect, which leads to our disconnect route. The spacing looks off so let's add this to the CSS.
```
.disconnect {
    margin-top: 1em !important;
    font-size: 0.7em;
}
```

Clicking it should remove the token, then connecting again should show it.

So now what we need to do is complete the Facebook oauth handshake to get the tokens.

The oauth handshake process works like this:
- 1: user clicks on connect facebook button
- 2: attempt connection to facebook
- 3: user authenticates with facebook
- 4: auth code comes back from facebook
- 5: auth code exchanged for access token

We'll trigger step 2 with our connectors/facebook function, then facebook will want to send us an auth code to a callback function, which will be another route.

In that route, we'd then save the token on authorization.

We will need our Facebook secrets etc so let's check they're loading properly. Import config into route:
`from config import Config`

Put this in one of the routes to check it's working:
`print(Config.CONNECTORS['facebook_app_id'])`

Let's start backwards and work on the call back first - this is when the user has authenticated and facebook is sending us an auth code.

Copy the connect route, and change it to this:
`@bp.route('/<platform>/callback')`

We're going to need to import request from flask, and requests and json libraries too.
`from flask import render_template, session, flash, redirect, url_for, request`
`import requests`
`import json`

Then what we write next goes in place of the token assignment.

First get the access code from the request from Facebook.

```
# Get authorization code Facebook sent back to you
code = request.args.get("code")
print("callback got it: ", code)
```

Then we need to construct the token URL where we exchange the code for a token.

This needs the following parameters:
- the app client
- the secret code for the app
- the access code
- the callback parm (where facebook will send the token)
```
# Construct the token URL
client_param = "?client_id=" + Config.CONNECTORS['facebook_app_id']
secret_param = "&client_secret=" + Config.CONNECTORS['facebook_app_secret']
code_param = '&code=' + code
callback_param = '&redirect_uri=' + request.base_url

token_url = Config.CONNECTORS['facebook_token_endpoint'] + client_param + secret_param + callback_param + code_param

print("trying url: ", token_url)
```

Then you need to get the token from the response.

```
# Get the token
token_response = requests.post(token_url)

# Parse the token
print("token dump:", json.dumps(token_response.json()))

token = token_response.json().get('access_token')
```

Then of course you need to save the token via teams as per before.

```
# Save the token
team = Team.get(session.get('team_id'))
team.facebook_connect(token)
```

You might also want to flash to the user if token didn't come back.

So add this to the top of the route: `token = None`

Then do this at the bottom before redirect.
```
if token:
        flash(f"{platform} connected", 'pink')
    else:
        flash(f"Error: {platform} not connected", 'red')

```

Great, there's a lot going on there but let's just move on to initiating the auth with facebook and then check if it all works.

The following code goes in the route for connect.

```
# Build URI for auth endpoint
client_param = "?client_id=" + Config.CONNECTORS['facebook_app_id']
callback_param = '&redirect_uri=' + request.base_url + '/callback'
state_param = '&state=' + session['csrf_token']
scope_param = "&scope=ads_read"

request_uri = Config.CONNECTORS['facebook_authorization_endpoint'] + client_param + callback_param + state_param + scope_param

return redirect(request_uri)
```
This is a lot simpler, and it just needs the app id from you. You can also pass the csrf token and check that on the backend. Note we're just asking for read access, but you might want to change the scope if you need to put ads live or make other changes.

First let's change some settings in Facebook to allow this to work.

Add the Facebook login product and change the `Embedded Browser OAuth Login` setting to YES

Add this to the Valid OAuth Redirect URIs
`https://127.0.0.1:5000/connectors/facebook/callback`
`https://fireflask-ef97c.uc.r.appspot.com/connectors/facebook/callback`

Now we have to trick facebook into thinking our local host is https.
- [http://blog.shea.io/facebook-authentication-for-flask-apps/](http://blog.shea.io/facebook-authentication-for-flask-apps/)
- [https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)
- [https://kracekumar.com/post/54437887454/ssl-for-flask-local-development/](https://kracekumar.com/post/54437887454/ssl-for-flask-local-development/)
- [https://zhangtemplar.github.io/flask/](https://zhangtemplar.github.io/flask/)
- [https://support.acquia.com/hc/en-us/articles/360004175973-Using-an-etc-hosts-file-for-custom-domains-during-development](https://support.acquia.com/hc/en-us/articles/360004175973-Using-an-etc-hosts-file-for-custom-domains-during-development)
- [https://support.acquia.com/hc/en-us/articles/360004175973-Using-an-etc-hosts-file-for-custom-domains-during-development](https://support.acquia.com/hc/en-us/articles/360004175973-Using-an-etc-hosts-file-for-custom-domains-during-development)

So we have to install pyOpenSSL
`pip install pyopenssl`
`pip freeze requirements.txt`

Then run flask but with an adhoc ssl certificate:
`flask run --cert=adhoc`

Now visit the https site and click through to ignore the warnings (advanced > accept the risk and continue).
https://127.0.0.1:5000/

Ok let's see if this works!

You should get a warning that you need to submit for review - shouldn't be needed just for testing, so you should be good as it is.

Check the token appears as usual, except this time it's a proper facebook token!

You can validate this by visiting `https://developers.facebook.com/tools/debug/accesstoken/`

Input the token and it'll tell you more info about it.

If you want to see if the ads permission worked properly, you can run a query in the Graph API Explorer here:
`https://developers.facebook.com/tools/explorer/`

Put your access token in, and put this link in the GET section: 
`me?fields=id,name,adaccounts{amount_spent,name}`

Then hit submit - you should be able to get a list of the ad accounts and spend the user has access to.

Note: this is why you shouldn't give your token to anyone - they can access any of your information just as if they had the password to your account!

Now we've got the ability to collect the token, let's connect this up properly
- write a new cloud function that pulls based on the facebook token of the user
- create a new dashboard that works based on the new connector

Before we write our cloud function, let's just test the endpoint with the Graph Explorer tool we were just using.

That way we can make sure it returns the data we need without having to continually upload our code.

If we want to know what parameters are available, we can take a look at the documentation.
`https://developers.facebook.com/docs/marketing-api/insights/parameters/v6.0#parameters-and-fields`

If we want to pull account level data, the end point is the account id prepended by `act_`, then ended with /insights. So for example
`act_10152696796219352/insights`

Then we just need to add the params, for example: 
- level (account, campaigns, adsets, ads) how you want the results broken down by structure
- fields (spend, impressions, inline_link_clicks, actions) this is the data we want to pull*
- date_preset (last_30d) this gives us the last 30 days data
- time_increment (1) this breaks the data out by day

*note: actions are where we can find our conversions, and inline_link_clicks is clicks out to our site.

The final query looks like this:
`act_10152696796219352/insights?level=account&fields=spend,impressions,inline_link_clicks,actions&date_preset=last_30d&time_increment=1`

It should give you back some data in the following format:
```
{
  "data": [
    {
      "spend": "1044.84",
      "impressions": "104770",
      "inline_link_clicks": "287",
      "actions": [
        {
          "action_type": "landing_page_view",
          "value": "97"
        },
        {
          "action_type": "comment",
          "value": "4"
        },
        {
          "action_type": "onsite_conversion.post_save",
          "value": "4"
        },
        {
          "action_type": "like",
          "value": "2"
        },
        {
          "action_type": "link_click",
          "value": "287"
        },
        {
          "action_type": "offsite_conversion.fb_pixel_initiate_checkout",
          "value": "91"
        },
        {
          "action_type": "offsite_conversion.fb_pixel_purchase",
          "value": "70"
        },
        {
          "action_type": "post",
          "value": "2"
        },
        {
          "action_type": "post_reaction",
          "value": "10"
        },
        {
          "action_type": "video_view",
          "value": "6988"
        },
        {
          "action_type": "post_engagement",
          "value": "7295"
        },
        {
          "action_type": "page_engagement",
          "value": "7297"
        },
        {
          "action_type": "omni_initiated_checkout",
          "value": "91"
        },
        {
          "action_type": "omni_purchase",
          "value": "70"
        },
        {
          "action_type": "initiate_checkout",
          "value": "91"
        },
        {
          "action_type": "purchase",
          "value": "70"
        }
      ],
      "date_start": "2020-07-20",
      "date_stop": "2020-07-20"
    },
    {
      "spend": "1064.23",
      "impressions": "98900",
      "inline_link_clicks": "266",
      "actions": [
        {
          "action_type": "landing_page_view",
          "value": "101"
        },
        {
          "action_type": "comment",
          "value": "3"
        },
        {
          "action_type": "onsite_conversion.post_save",
          "value": "5"
        },
        {
          "action_type": "like",
          "value": "1"
        },
        {
          "action_type": "link_click",
          "value": "266"
        },
        {
          "action_type": "offsite_conversion.fb_pixel_initiate_checkout",
          "value": "111"
        },
        {
          "action_type": "offsite_conversion.fb_pixel_purchase",
          "value": "86"
        },
        {
          "action_type": "post",
          "value": "4"
        },
        {
          "action_type": "post_reaction",
          "value": "12"
        },
        {
          "action_type": "video_view",
          "value": "6895"
        },
        {
          "action_type": "post_engagement",
          "value": "7185"
        },
        {
          "action_type": "page_engagement",
          "value": "7186"
        },
        {
          "action_type": "omni_initiated_checkout",
          "value": "111"
        },
        {
          "action_type": "omni_purchase",
          "value": "86"
        },
        {
          "action_type": "initiate_checkout",
          "value": "111"
        },
        {
          "action_type": "purchase",
          "value": "86"
        }
      ],
      "date_start": "2020-07-21",
      "date_stop": "2020-07-21"
    }
  ]}
```

If that looks right, then it's time to build our cloud function.

Create a new folder called "get_facebook_data" and create a main.py file inside.

```
def main(request):
    return "hello"

if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)
    app.route('/')(lambda: main(request))
    app.run(debug=True)
```

Now we want to exit the flask server
`CTRL C`

Then deactivate our virtual env
`deactivate`

Then create your new virtual env
```
cd functions
python -m venv get_facebook_data_venv
.\get_test_facebook_venv\Scripts\activate
```

Now let's install flask
`pip install flask`

as well as facebook's sdk
`pip install facebook_business`

Great, that should be the only requirements, so we can now pip freeze.
`pip freeze > get_facebook_data/requirements.txt`

To check it's working, run this:
`python get_facebook_data/main.py`

If you visit `http://127.0.0.1:5000/` you should see it says `hello`

Now let's set up the app_id and secret - we'll add them to the function deployment later, but for testing we need to set them like this:

`$env:FACEBOOK_APP_ID="123456"`
`$env:FACEBOOK_APP_SECRET="abcdef"`

Now set the file to pull from the os.environ to get the secret and id.
`import os`
then in the main function:
```
facebook_app_id = os.environ.get('FACEBOOK_APP_ID')
facebook_app_secret = os.environ.get('FACEBOOK_APP_SECRET')
```

We also want to be able to return the data in JSON format, so add import jsonify from flask.
`from flask import jsonify`

```
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
return jsonify(data)
```

Great so now test it's working.
`python get_facebook_data/main.py`

If we visit `http://localhost:5000/?access_token=testtoken123`

We should see our hardcoded data.

Now let's pull the real data from Facebook itself!

First install the library by adding these imports.
```
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
```

This line handles the initialization with the user's access token
`FacebookAdsApi.init(facebook_app_id, facebook_app_secret, access_token)`

We also need to grab the account id
`account_id = request.args.get('account_id')`

Then the meat of the function follows the same parameters as what we set up before in the open graph explorer.
```
# Make a call to the Facebook API
my_account = AdAccount('act_'+account_id)
fields = ['spend', 'impressions', 'inline_link_clicks', 'actions']
params = {'level':'account', 'date_preset':'last_30d'}
insights = my_account.get_insights(fields=fields, params=params)[0]
data = dict(insights)
```

Let's give it a try.
`python get_facebook_data/main.py`

Visit `http://localhost:5000/?access_token=<token>&account_id=<account>`

Just a couple more changes:
- add the time increments
- allow start and end dates

To allow time increments, add this to the params
`params = {'level':'account', 'date_preset':'last_30d', 'time_increment':1}`

Then we need to loop through the cursor object Facebook returns, to get a list of dictionaries.

```
data = []
for day in insights:
    data.append(dict(day))
```

Then to choose date range, we need to add this to the params.
`'time_range': {'since': '2019-01-01', 'until': '2019-01-05'}`

Now let's accept these dates via the function params.

Grab the variables from the request.
```
date_start = request.args.get('date_start')
date_stop = request.args.get('date_end')
```

Then insert them:
`'time_range': {'since': date_start, 'until': date_end}`

Visit `http://localhost:5000/?access_token=<token>&account_id=<account>&date_start=2020-01-01&date_end=2020-01-20`

Perfect, but the data is coming out a little different than we wanted. Remember the format we had before?

[{
    "date": "2020-01-09",
    "spend": "8000.00",
    "clicks": "9900",
    "impressions": "3050000",
    "conversions": "1200"
}

So let's add a mapping to make that match, so we won't have to change our frontend.

```
for day in insights:
    format_data = {}
    format_data['date'] = day['date_start']
    format_data['impressions'] = day['impressions']
    format_data['clicks'] = day['inline_link_clicks']
    format_data['spend'] = day['spend']
    format_data['conversions'] = day['actions']
    data.append(format_data)
```

But we also need a way to condense actions down to just the one conversion metric we care about.

So let's pass a conversion event to this function too.
`conversion_event = request.args.get('conversion_event')`

Then we need to use it to process the actions dictionary and choose the right event.
```
# Pull out conversion metric
conversions = [action.get('value') for action in day['actions'] if action.get('action_type') == conversion_event]

if conversions:
    format_data['conversions'] = conversions[0]
else:
    format_data['conversions'] = "0"

# Append to the data list
data.append(format_data)
```

Visit `http://localhost:5000/?access_token=<token>&account_id=<account>&date_start=2020-01-01&date_end=2020-01-20&conversion_event=purchase`

It's also worth testing it with a conversion event that doesn't exist, just to check it correctly gives you 0.

Now let's deploy this with the environment variables. Note we changed the function name to main now so we need to update the entry point also.

`gcloud beta functions deploy get_facebook_data --trigger-http --runtime python37 --project fireflask-ef97c --source C:\Users\Hammer\Documents\Projects\FireFlask\functions\get_facebook_data --allow-unauthenticated --entry-point=main --update-env-vars APP_ID=123456,APP_SECRET=abcdef`

Once we run this, we should be able to test it by visiting `https://us-central1-fireflask-ef97c.cloudfunctions.net/get_facebook_data?access_token=<token>&account_id=<account>&date_start=2020-01-01&date_end=2020-01-20&conversion_event=purchase`

Now we're done testing the function, we can move on back to integrating it with our dashboard.

`CTRL C` to exit the flask server
`deactivate` to exit the venv
`cd ..` to get back to the right folder
`venv\Scripts\activate` to reactivate your main venv

Copy the dashboard function in routes and swap out the name to this:
```
@bp.route('/facebook', methods=['GET', 'POST'])
@login_required
def facebook_dashboard():
```

Change the cloud function:
`url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_facebook_data"`

Hard code the conversion event for now:
`"conversion_event": "purchase"`

Then pull the token from team
`"access_token": team.facebook_token,`

Then let's test it out
`flask run --cert=adhoc`

Remember to update your account id and get a fresh access token.

Then visit `https://127.0.0.1:5000/charts/facebook`

Let's tidy this up a bit to make it more useful.

Add conversions and cpa to the facebook dashboard route, and make it render a different dashboard template.

```
spend = sum([float(row['spend']) for row in data])
conversions = sum([float(row['conversions']) for row in data])
cpa = round(spend / conversions, 2)

return render_template(
    'charts/facebook_dashboard.html', 
    title='Facebook Dashboard', 
    data=data, 
    spend=spend,
    conversions=conversions,
    cpa=cpa, 
    form=form, 
    account_id=account_id
)
```

Create that new facebook_dashboard.html file and change the cards to 
```
<div class="row">
    <!-- Metric Score Card -->
    <div class="col s4">
        {% include 'charts/_card_spend.html' %}
    </div>

    <!-- Metric Score Card -->
    <div class="col s4">
        {% include 'charts/_card_conversions.html' %}
    </div>

    <!-- Metric Score Card -->
    <div class="col s4">
        {% include 'charts/_card_cpa.html' %}
    </div>
</div>
```

Then create a new card file for each, like this:
```
<div class="card">
    <div class="card-content">
        <p>CONVERSIONS</p>
        <span class="card-title grey-text text-darken-4">
            {{ "{:,.0f}".format(conversions) }}
        </span>
    </div>
</div>
```

You should also change the line chart to 

```
<!-- Chart JS line chart -->
<div class="col s12 m6 l6">
    {% include 'charts/_line_cpa.html' %}
</div>
```

This is how it'd look with modifications to show CPA instead of spend.
```
<div class="card-panel">
    <canvas id="lineChart" width="200" height="100"></canvas>
</div>

{% block javascript %}
<script>
    var chartData = chartData || JSON.parse('{{ data|tojson }}');
    var data = [];
    var labels = [];
    for (i=0; i<chartData.length; i++) {
        var spend = chartData[i]['spend']
        var conversions = chartData[i]['conversions']

        data.push(spend/conversions);
        labels.push(chartData[i]['date']);
    }
    
    var ctx = document.getElementById('lineChart').getContext('2d');
    var lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'CPA',
                data: data,
                fill: true,
                lineTension: 0.1,
                backgroundColor: "rgba(75,192,192,0.4)",
                borderColor: "rgba(75,192,192,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                spanGaps: false
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    
</script>
{% endblock %}
```

We should also add a link through to the Facebook dashboard in the teams view page.

```
<div class="col s12 m8 l7">
    <a href="{{ url_for('charts.facebook_dashboard') }}">
        <div class="card-panel">
            <i class="fa fa-facebook-f fa-lg blue-text"></i>
            &nbsp;Go to Facebook dashboard >
        </div>
    </a>    
</div>
```

A couple of final bits - let's add the conversion event to the team page.

First add it to the model:
```
class Team():
    def __init__(self, id_, name, account_id, conversion_event, facebook_token=None):
        self.id = id_
        self.name = name
        self.account_id = account_id
        self.facebook_token = facebook_token
        self.conversion_event = conversion_event
    
    @staticmethod
    def get(team_id):
        team_data = pyr_db.child('teams').child(team_id).get().val()
        team = Team(
            id_=team_id, 
            name=team_data['name'],
            account_id=team_data.get('account_id'),
            conversion_event=team_data.get('conversion_event'),
            facebook_token=team_data.get('facebook_token')
        )
        return team

    @staticmethod
    def create(name):
        team_res = pyr_db.child('teams').push({
            "name": name
        })
        team_id = team_res['name'] # api sends id back as 'name'
        print('Sucessfully created new team: {0}'.format(team_id))

        team = Team.get(team_id)
        return team

    def update(self, name, account_id, conversion_event):
        pyr_db.child('teams').child(self.id).update({
            "name": name,
            "account_id": account_id,
            "conversion_event": conversion_event 
        })

        self.name = name
        self.account_id = account_id
        self.conversion_event = conversion_event

    def facebook_connect(self, token):
        pyr_db.child('teams').child(self.id).update({
            "facebook_token": token,
        })

        self.facebook_token = token
```

Add it to the route.
```
@bp.route('/<team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):

    role = Membership.user_role(current_user.id, team_id)
    if role not in ["ADMIN", "OWNER"]:
        abort(401, "You don't have access to edit this team.")

    form = TeamForm()

    team = Team.get(team_id)

    if form.validate_on_submit():
        name = form.name.data
        account_id = form.account_id.data
        conversion_event = form.conversion_event.data

        #edit a team
        try:
            team.update(name, account_id, conversion_event)

            # Update successful
            flash('Team {}, updated with name={}'.format(
                 team.id, team.name), 'teal')

            return redirect(url_for('teams.view_team', team_id=team.id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')

    form.name.data = team.name
    form.account_id.data = team.account_id
    form.conversion_event.data = team.conversion_event
        
    return render_template('teams/edit_team.html', title='Edit Team', form=form, 
        team=team)
```

Then to view team.
```
<tr>
    <td>Conversion Event</td>
    <td>{{ team.conversion_event }}</td>
</tr> 
```

Then we've got the edit page.
```
<p class="input-field">
    {{ form.conversion_event.label }}<br>
    {{ form.conversion_event(size=32, class_="validate") }}<br>
    {% for error in form.conversion_event.errors %}
    <span class="helper-text" data-error="[{{ error }}]" data-success=""></span>
    {% endfor %}
</p>
```

Finally the form.
```
conversion_event = StringField('Conversion Event')
```

Then you just need to update the route to accept the conversion event from the team in the session.

```
if not session.get('team_id'):
    # No team selected
    flash("Please select a team", 'orange')
    return redirect(url_for('teams.list_teams'))
else:
    team = Team.get(session.get('team_id'))
    account_id = team.account_id
    conversion_event = team.conversion_event

    if not account_id:
        # No account id for team
        flash("Please ask account owner to update Account ID", 'orange')
        return redirect(url_for('teams.edit_team', team_id=team.id))
    
    if not conversion_event:
        # No account id for team
        flash("Please ask account owner to update Conversion Event", 'orange')
        return redirect(url_for('teams.edit_team', team_id=team.id))

# Run the cloud function
url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_facebook_data"
payload = {
    "access_token": team.facebook_token,
    "account_id": account_id,
    "date_start": start_date,
    "date_end": end_date,
    "conversion_event": conversion_event
```

Also let's wrap the whole call in a try catch, so the application doesn't just quit on us when something goes wrong.

```
 # Run the cloud function
try:
    url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_facebook_data"
    payload = {
        "access_token": team.facebook_token,
        "account_id": account_id,
        "date_start": start_date,
        "date_end": end_date,
        "conversion_event": conversion_event
        }
    response = requests.get(url, params=payload)
    data = json.loads(response.text)
except Exception as e:
        # No account id for team
    flash(f"Error: {e}", 'red')
    flash("Make sure Account ID, Conversion Event are correct", 'orange')
    return redirect(url_for('teams.edit_team', team_id=team.id))
```

One more thing to do - you may have noticed that the access token doesn't last very long, just a few hours.

You can exchange the token for a long-lived token, which lets you query for 60 days (or longer, because it's refreshed on every call).

More info can be found here: [https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing/](https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing/)

The API call goes like this:
`https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}`

So in our routes file let's do this

```
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
```

If you copy the access token from the database and run it through facebook's debugger, you should see that it expires in 2 months.
`https://developers.facebook.com/tools/debug/accesstoken`

There's obviously more we could do here, and we could run through adding more connectors to the page, but for now this is a good stopping point, and we can now access really anything we want in Facebook.


