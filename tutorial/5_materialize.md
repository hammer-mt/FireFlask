### 5: Adding Materialize css / js

Now it's time to make our website look pretty.

We're using Materialize instead of Bootstrap because it looks a bit more professional - bootstrap is overused and is a sign of a bad website almost these days.

We're going to be following this tutorial by The Net Ninja: 

https://www.youtube.com/playlist?list=PL4cUxeGkcC9jUPIes_B8vRjn1_GaplOPQ

His source code is here:
https://github.com/iamshaunjp/firebase-auth/tree/lesson-3

He also has a more in-depth Materialize CSS tutorial here: https://www.youtube.com/playlist?list=PL4cUxeGkcC9gGrbtvASEZSlFEYBnPkmff

Here's the link to the Materalize framework: https://materializecss.com/

We're using this rather than bootstrap, because we want to make the application more modern looking and since we're using the Google stack for everything else, why not use it for the CSS as well (Material design, which Materialize is based off, is a Google invention).

First let's update the top of our base.html to follow the standard base document.

Note you can get this by typing 'doc' then hitting tab in VSCode.

```
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
```

Next you want to get the materalize css and js CDNs from the Materalize site.

```
<!-- Compiled and minified CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">

<!-- Compiled and minified JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
```

They go in the head of the base.html page, above the title, below the meta.

It also helps to add a meta description at this point too.

```
{% if desc %}
<title>{{ desc }}</title>
{% else %}
<meta name="description" content="Fireflask is a boilerplate template for spinning up a Python Flask application with a Firebase NoSQL database / cloud function backend, and Materalize CSS."/>
{% endif %}
```

We should also update the index.html with this description.

```
{% extends "base.html" %}

{% block content %}
    {% if current_user.is_authenticated %}
    <h1>Hi, {{ current_user.name }}!</h1>
    {% else %}
    <h1>FireFlask</h1>
    <p>Fireflask is a boilerplate template for spinning up a Python Flask application with a Firebase NoSQL database / cloud function backend, and Materalize CSS.</p>
    {% endif %}
{% endblock %}
```

It's probably worth updating the readme too.

Now let's update the body.

Add the class grey lighten-3 to the body element.
`<body class="grey lighten-3">`

Now copy and paste this navbar across.

```
<!-- NAVBAR -->
<nav class="z-depth-0 grey lighten-4">
<div class="nav-wrapper container">
    <a href="#" class="brand-logo">
    <img src="img/logo.svg" style="width: 180px; margin-top: 10px;">
    </a>
    <ul id="nav-mobile" class="right hide-on-med-and-down">
        <li class="logged-in">
        <a href="#" class="grey-text modal-trigger" data-target="modal-account">Account</a>
        </li>
        <li class="logged-in">
        <a href="#" class="grey-text" id="logout">Logout</a>
        </li>
        <li class="logged-in">
        <a href="#" class="grey-text modal-trigger" data-target="modal-create">Create Guide</a>
        </li>
        <li class="logged-out">
        <a href="#" class="grey-text modal-trigger" data-target="modal-login">Login</a>
        </li>
        <li class="logged-out">
        <a href="#" class="grey-text modal-trigger" data-target="modal-signup">Sign up</a>
        </li>
    </span>
    </ul>
</div>
</nav>
```

Delete all the modal stuff (data-target) as we're not using that right now.
`data-target="modal-account"`

Change the brand logo to what you want.

```
<a href="#" class="brand-logo">
    <span class="grey-text">🔥⚗️ FireFlask</span>
</a>
```

Get rid of the guides link as we don't use that.
```
<li class="logged-in">
<a href="#" class="grey-text">Create Guide</a>
</li>
```

Update the hrefs with the correct urlfor links
`<a href="{{ url_for('index') }}" class="brand-logo">`

You can also get rid of the class="logged-out" stuff
`<li class="logged-out">`

Now add in your user authentication.

`{% if current_user.is_authenticated %}`

Add the following class to the signup button.
`class="waves-effect waves-light btn"`

Then almost the same to the sign out button.

`"waves-effect waves-light grey lighten-2 grey-text btn-flat"`

So the full navbar should look like this
```
<!-- NAVBAR -->
<nav class="z-depth-0 grey lighten-4">
    <div class="nav-wrapper container">
        <a href="{{ url_for('index') }}" class="brand-logo">
            <span class="grey-text">🔥⚗️ FireFlask</span>
        </a>
        <ul id="nav-mobile" class="right hide-on-med-and-down">
            {% if current_user.is_authenticated %}
            <li>
                <a href="{{ url_for('sign_out') }}" class="waves-effect waves-light grey lighten-2 grey-text btn-flat">Sign Out</a>
            </li>
            {% else %}
            <li>
                <a href="{{ url_for('sign_in') }}" class="grey-text">Sign In</a>
            </li>
            <li>
                <a href="{{ url_for('sign_up') }}" class="waves-effect waves-light btn">Sign Up</a>
            </li>
            {% endif %}
        </span>
        </ul>
    </div>
</nav>
```

Now to add styling to the footer, we have to change the base.html

Add this to the header:
```
<style>
    body {
        display: flex;
        min-height: 100vh;
        flex-direction: column;
    }
    main {
        flex: 1 0 auto;
    }
</style>
```

Put your flash messages and content block in a main tag
```
<main>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        {% for category, message in messages %}
        <div class="alert alert-{{ category }} alert-dismissible" role="alert">
            <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            {{ message }}
        </div>
        {% endfor %}
        {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
</main>
```

Ok now change the footer to this:

```
<footer class="page-footer grey lighten-4">
    <div class="container">
        {% if current_user.is_authenticated %}
        <p class="grey-text">Current user: {{ current_user.id }}</p>
        {% else %}
        <p class="grey-text">Current user: Anonymous</p>
        {% endif %}
    </div>
</footer>
```

In the form templates change the errors from
`<span style="color: red;">[{{ error }}]</span>`

over to the new format for materialize

`<span class="helper-text" data-error="[{{ error }}]" data-success=""></span>`


We don't have alerts in materalize, so we need to change them to toasts, which are javascript.

This is how it works - find the alert messages part pf base.html
```
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
{% for category, message in messages %}
<div class="alert alert-{{ category }} alert-dismissible" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
    {{ message }}
</div>

{% endfor %}
{% endif %}
{% endwith %}
{% block content %}{% endblock %}
```

Then replace it with this:
```
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
{% for category, message in messages %}
<script>
    (function () {
        M.toast({html: "{{ message }}", classes: "{{ category }}"})
    })();
</script>
{% endfor %}
{% endif %}
{% endwith %}
{% block content %}{% endblock %}
```

Now we just need to change the categories to the colors we want to style these as in routes.py

For example:
`flash('Error: {}'.format(e), 'danger')`

to this
`flash('Error: {}'.format(e), 'red')`

Or
```
flash('User {}, created with id={}'.format(
    current_user.email, current_user.id),
    'teal'
)
```

Make sure you change the errors in the signup and signin routes to print out the actual text or it'll break

```
except Exception as e:
    print(e)
    error_json = e.args[1]
    error = json.loads(error_json)['error']['message']
    flash("Error: {}".format(error), 'red')
```

Here is what your signup file should look like

```
{% extends "base.html" %}

{% block content %}
<h3>Sign Up</h3>
<p>Enter your name email address and password to sign up.</p>

<div class="row">
    <div class="col s12 m5">
        <div class="card-panel">
            <form action="" method="post">
                {{ form.hidden_tag() }}
                <p class="input-field">
                    {{ form.name.label }}<br>
                    {{ form.name(size=32, class_="validate") }}<br>
                    {% for error in form.name.errors %}
                    <span class="helper-text" data-error="[{{ error }}]" data-success=""></span>
                    {% endfor %}
                </p>
                <p class="input-field">
                    {{ form.email.label }}<br>
                    {{ form.email(size=32, class_="validate") }}<br>
                    {% for error in form.email.errors %}
                    <span class="helper-text" data-error="[{{ error }}]" data-success=""></span>
                    {% endfor %}
                </p>
                <p class="input-field">
                    {{ form.password.label }}<br>
                    {{ form.password(size=32, class_="validate") }}<br>
                    {% for error in form.password.errors %}
                    <span class="helper-text" data-error="[{{ error }}]" data-success=""></span>
                    {% endfor %}
                </p>
                <p class="right-align">
                    <button type="submit" name="btn" class="waves-effect waves-light btn teal">
                    SIGN UP
                    </button>
                </p>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

Feel free to add more sections to the homepage.
```
<div class="divider"></div>
<br>
<div class="row center">
    <div class="col s12 m8 offset-m2">
        <div class="commit">
            Check out the project on Github:
            <a href="https://github.com/mjt145/FireFlask/tree/master">mjt145/FireFlask/tree/master</a>
        </div>
    </div>
</div>
<div class="divider"></div>
<div class="section">
    <div id="team" class="section">
        <h3 class="header">Meet the Author</h3>
        <p>Who created FireFlask? Oh and by 'create', we mean 'hack together from multiple tutorials'.</p>
        <br>
        <div class="row">
            <div class="col s12 m3 center-on-small-only">
                <div class="image-container">
                <img src="{{ url_for('static', filename='images/mike.jpg') }}" class="circle responsive-img">
            </div>
            </div>
            <div class="col s12 m9">
                <h4>Michael Taylor</h4>
                <p>Is a marketer who learned to code. Co-founder of Ladder.io and Saxifrage.xyz, 
                    he has 10 years experience in growth marketing and has been coding in evenings 
                    and weekends for the past 5. He created FireFlask to make it easy to take his 
                    scripts out of Jupyter Notebooks and stand them up as web applications, without 
                    having to mess around with SQL, database migrations or scaling infrastructure.</p>
            </div>
        </div>
    </div>
</div>
<div class="divider"></div>   
```

Now let's make the navbar active based on what page you're on.

First let's add JQuery to the base header
```
<!-- Compiled and minified JQuery -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
```

Now let's add the following JQuery to the base.html template.
```
<script>
    $(document).ready(function () {
    $("#{{request.endpoint}}").addClass("active"); })
</script>  
```

Now all we need to do to add an id with the same name as the function for that route, in any navlinks where we want this to show as active.

```
<li id="sign_in">
    <a href="{{ url_for('sign_in') }}" class="grey-text">Sign In</a>
</li>
<li id="sign_up">
    <a href="{{ url_for('sign_up') }}" class="waves-effect waves-light btn">Sign Up</a>
</li>
```

Finally let's build in a dropdown menu.

```
<!-- Dropdown Structure -->
<ul id="dropdown1" class="dropdown-content">
    <li class="index"><a href="{{ url_for('index') }}">Home</a></li>
    <li><a href="#!">Account</a></li>
    <li class="divider"></li>
    <li>
        <a href="{{ url_for('sign_out') }}" class="grey-text">Sign Out</a>
    </li>
</ul>
<!-- Dropdown Trigger -->
<li>
    <a class="dropdown-trigger grey-text" href="#!" data-target="dropdown1">Settings<i class="material-icons right">arrow_drop_down</i></a>
</li>
```

In the above we moved the signout link to the settings dropdown, and added a placeholder for account updates.

