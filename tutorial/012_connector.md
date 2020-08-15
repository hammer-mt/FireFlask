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

- if a user visits the connectors page without a team selected, it prompts them to choose a team
- when on the team page, there will be a link to connectors, and the link in the navbar will work
- visiting the connectors page will list all connectors for that user and team
- there will be one connector per platform (in this case for now just Facebook Ads)
- if the connector isn't connected, you have to option to connect, if it is, you can reconnect
- clicking connect will take you through the oauth process to get and store a token
- reconnect will do the same, except the old token that was stored will be replaced
- the token will be stored in a connection option in the database, with team id and user id
- the connections page won't be visible for anyone who's not the owner of the account

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




Now we've got the ability to collect the token, let's connect this up properly
- write a new cloud function that pulls based on the facebook token of the user
- create a new dashboard that works based on the new connector
- anyone on the team will see data pulled from that connection set by the owner
- if they aren't the owner, they will get a prompt to contact the owner to connect
