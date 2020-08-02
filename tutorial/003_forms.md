### 3: Set up the web forms
Next step is to accept input from users, for example to publish posts or sign up via web forms. For this we use WTForms.

First let's install WTForms and update requirements
`pip install flask-wtf`
`pip freeze > requirements.txt`

Now create a new branch in git as before
`git checkout -b "forms"`

Change the __init__.py file to this
```
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
```

That will let you import a config file, which should look like this:
```
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
```

It should be in the top level directory.

Now create a file called forms.py in the app folder, with the following contents:
```
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
```

The next step is to add the template for the login page, as login.html:
```
{% extends "base.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}
        </p>
        <p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

Now let's create a view function in the routes.py file

Add this to the top
`from app.forms import LoginForm`
and then this to the bottom:
```
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
```

To make it easy to navigate to, include the link to the login page from the nav in the base.html template

```
<div>
    FireFlask:
    <a href="/index">Home</a>
    <a href="/login">Login</a>
</div>
```

Now we just need to add a way to handle the form data submitted. In the routes.py file we should change the login path to this:
```
from flask import render_template, flash, redirect

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
```

Note the import line should replace the one at the top, and then the rest of the code replaces just the login route (leave the other routes there)

Finally let's add the flash message to the base template so they show on any page.

```
<html>
    <head>
        {% if title %}
        <title>{{ title }} - FireFlask</title>
        {% else %}
        <title>FireFlask</title>
        {% endif %}
    </head>
    <body>
        <div>
            FireFlask:
            <a href="/index">Home</a>
            <a href="/login">Login</a>
        </div>
        <hr>
        {% with messages = get_flashed_messages() %}
        {% if messages %}
        <ul>
            {% for message in messages %}
            <li>{{ message }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </body>
</html>
```

We also need to pass the error messages back to the form as well, in the login.html templates so they're rendered when users enter something wrong.

```
{% extends "base.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}<br>
            {% for error in form.username.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}<br>
            {% for error in form.password.errors %}
            <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </p>
        <p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

Last thing to tidy up, is the links, because they shouldn't be hardcoded and instead should use url_for().

Change the two links in the base.html template:
```
<a href="{{ url_for('index') }}">Home</a>
<a href="{{ url_for('login') }}">Login</a>
```

Import url_for in the routes.py
`from flask import render_template, flash, redirect, url_for`

Change the redirect on form validate on submit
`return redirect(url_for('index'))`


Random note: if you set `FLASK_DEBUG=1` in the .flaskenv, you don't have to keep restarting the server to see changes.

The correct flow to integrate a branch and push changes to master is as follows:

Check you're on the right branch
`git branch`

Make sure you're up to date with your commits
`git status`
`git commit -m "added forms to the application"`

Push the branch changes upstream to github
`git push --set-upstream origin forms`

Now you can integrate the branch locally, first checkout master branch
`git checkout master`

Pull down from github to make sure you're up to date
`git pull origin master`

Now merge the forms branch into your local master
`git merge forms`

Check out the git log and see where you're at
`git log --oneline`

Check out the diff if needed by getting the hash from git log
`git diff 30519e4`
exit with `q`

Once you're happy you can push to master
`git push origin master`

Now delete the branch you don't need anymore, locally and remotely
`git branch -d forms`
`git push origin --delete forms`