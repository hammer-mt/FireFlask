### 12: Connecting a User's Facebook account

Now for a big leap in our applications usefulness - connecting to an external API via oauth. We'll use the Facebook API for this, and it will involve letting a user authenticate via Facebook, then passing that token to a cloud function, which we'll modify from the test one we made to actually pull data from facebook. 

- [https://realpython.com/flask-google-login/](https://realpython.com/flask-google-login/)
- [https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask](https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask)

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
@bp.route('/connections/<platform>')
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
@bp.route('/connections/<platform>')
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

So now what we need to do is complete the Facebook oauth handshake to get the tokens.

The oauth handshake process works like this:
- 1: user clicks on connect facebook button
- 2: attempt connection to facebook
- 3: user authenticates with facebook
- 4: auth code comes back from facebook
- 5: auth code exchanged for access token




Now we've got the ability to collect the token, let's connect this up properly
- write a new cloud function that pulls based on the facebook token of the user
- create a new dashboard that works based on the new connector
- anyone on the team will see data pulled from that connection set by the owner
- if they aren't the owner, they will get a prompt to contact the owner to connect
