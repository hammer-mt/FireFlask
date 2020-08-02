### 2: Set up the initial Flask application
Now it's time to create our first working application.

`mkdir app`


Make a new file in the app folder called __init__.py
```
from flask import Flask

app = Flask(__name__)

from app import routes
```

Next we need to add the routes file which determines where traffic is sent
```
from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
```

Finally to make the app work, you have to have a script at the top level that you'd run to start the application.

`from app import app`

Now you just need to tell windows what file to run for your flask app

`set FLASK_APP=fireflask.py`

You can run the app using this commmand

`flask run`

Then just press CTRL + c to exit

To make the environment variable be remembered across sessions, install python-dotenv

`pip install python-dotenv`

Remember to freeze your requirements after installing

`pip freeze > requirements.txt`

Then add a .flaskenv file to the top level

`FLASK_APP=fireflask.py`

Make sure you add .flaskenv to your gitignore

Add the changes to git and commit

From now on we're going to make changes in branches and then merge to master. Create a new branch and check it out.

`git checkout -b "templates"`

Then see all your branches here
`git branch`

Switch back to head like this
`git checkout master`

To push the branch to github now you run this
`git push --set-upstream origin templates`

If you need to add deletes to git then do this
`git add -u .`

The correct workflow to integrate it back again is this
`git checkout master`
`git pull origin master`
`git merge templates`
`git push origin master`

Then you can delete the branch like this
`git branch -d templates`
`git push origin --delete templates`

Ok now onto the templates changes. First change the routes.py file to return some HTML.
```
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return '''
<html>
    <head>
        <title>Home Page - FireFlask</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
</html>'''
```

If you run the flask server and go to http://127.0.0.1:5000/ you'll see it now says 'Hello Miguel'

Next step is to abstract away that HTML into a different file.
`mkdir app/templates`

In app/templates make a html file called index.html
```
<html>
    <head>
        <title>{{ title }} - FireFlask</title>
    </head>
    <body>
        <h1>Hello, {{ user.username }}!</h1>
    </body>
</html>
```

Now go back to routes.py and change it to this
```
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)
```

Next let's try out conditional statements. Change the template to this:
```
<html>
    <head>
        {% if title %}
        <title>{{ title }} - FireFlask</title>
        {% else %}
        <title>Welcome to FireFlask!</title>
        {% endif %}
    </head>
    <body>
        <h1>Hello, {{ user.username }}!</h1>
    </body>
</html>
```

If we want to add loops, this is what we do to the routes.py to add a list of dictionarys we can loop through.
```
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Michael'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
```

Now in the template we need to change it to loop through the posts
```
<html>
    <head>
        {% if title %}
        <title>{{ title }} - FireFlask</title>
        {% else %}
        <title>Welcome to FireFlask</title>
        {% endif %}
    </head>
    <body>
        <h1>Hi, {{ user.username }}!</h1>
        {% for post in posts %}
        <div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
        {% endfor %}
    </body>
</html>
```

The next thing we'll want to do is set up some template inheritance, so we can have a nav bar.

Create a new html file called base.html in templates
```
<html>
    <head>
      {% if title %}
      <title>{{ title }} - FireFlask/title>
      {% else %}
      <title>Welcome to FireFlask</title>
      {% endif %}
    </head>
    <body>
        <div>FireFlask: <a href="/index">Home</a></div>
        <hr>
        {% block content %}{% endblock %}
    </body>
</html>
```

The block content part allows you to pull in other html files. Now we can simplify index.html and update the nav bar across every file in future.

```
{% extends "base.html" %}

{% block content %}
    <h1>Hi, {{ user.username }}!</h1>
    {% for post in posts %}
    <div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div>
    {% endfor %}
{% endblock %}
```