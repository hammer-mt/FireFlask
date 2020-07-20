### 7: Improving User Profiles

We have basic authentication now, but we don't have the ability to reset password, update your name / email / password, add a profile pic, or validate user's email.

Let's do password reset first.

In the /sign_up page, add this to the bottom of the 'col s12 m5' div the card is in.
`<a href="{{ url_for('auth.reset_password') }}" class="right">Forgot Password?</a>`

Now we need to make a new view that handles both resetting the password, and showing the reset form. This goes in the auth/routes.py file.

```
@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data

        #reset password
        try:
            User.reset(email)

            # Reset successful
            flash('Password reset for {}'.format(
                email), 'teal')
            return redirect(url_for('auth.sign_in'))

        except Exception as e:
            # Reset unsuccessful
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            flash("Error: {}".format(error), 'red')
            
            return render_template('auth/reset_password.html', title='Reset Password', form=form)
        
    return render_template('auth/reset_password.html', title='Reset Password', form=form)
    ```
Also remember to add ResetPasswordForm to your imports.

Now let's make the form, which is quite simple and goes in the auth/forms.py

```
class ResetPasswordForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('RESET PASSWORD')
```

We also need to update the User model to add the password reset method in models.py.

```
@staticmethod
    def reset(email):
        pyr_auth.send_password_reset_email(email)
```

Last part is adding the template for reset password in templates/auth. We can pretty much just copy the sign in template.

```
{% extends "main/base.html" %}

{% block content %}
<h3>Reset Password</h3>
<p>Enter your email address to reset password.</p>

<div class="row">
    <div class="col s12 m5">
        <div class="card-panel">
            <form action="" method="post">
                {{ form.hidden_tag() }}
                <p class="input-field">
                    {{ form.email.label }}<br>
                    {{ form.email(size=32, class_="validate") }}<br>
                    {% for error in form.email.errors %}
                    <span class="helper-text" data-error="[{{ error }}]" data-success=""></span>
                    {% endfor %}
                </p>
                <p class="right-align">
                    <button type="submit" name="btn" class="waves-effect waves-light btn orange">
                    RESET PASSWORD
                    </button>
                </p>
            </form>
        </div>
        <a href="{{ url_for('auth.sign_in') }}">< back to Sign In</a>
    </div>
</div>         
{% endblock %}
```

That should all now work.

Now let's set up the flow to authenticate an email address on signup.

First I'm going to move the users model to the auth section to tidy up.

Once you move the file, just make sure everywhere is updated like this:
`from app.models import User`
to 
`from app.auth.models import User`

You need to change it in auth/routes.py and delete the reference in app/__init__.py

Ok so let's add the basics of email verification - we probably won't do much with this right now, but we at least want to send on account creation.

In the auth/models.py add this to user Create method
```
# send verification
pyr_user = pyr_auth.sign_in_with_email_and_password(email, password)
pyr_auth.send_email_verification(pyr_user['idToken'])

print("Sent email verification")
```

You also need to add this to the rest of the model wherever you init a user.
`verified=firebase_user.email_verified`

Except the auth method, where you do this:
```
is_verified = pyr_user_info['users'][0]['emailVerified']

if not is_verified:
    # send verification
    pyr_auth.send_email_verification(pyr_user['idToken'])
    print("Sent email verification")

print('Sucessfully signed in user: {0}'.format(pyr_user['localId']))
flask_user = User(
    uid=pyr_user['localId'],
    email=pyr_user['email'],
    name=pyr_user['displayName'],
    verified=is_verified
)
```

Now we should just need to add to the base template a header for logged in users that tells them to verify if they haven't. This goes above the navbar, below the body.

```
{% if current_user.is_authenticated and not current_user.verified %}
<p id="verifyEmail" class="center-align red lighten-4">
    Please verify your email address. &nbsp;
    <a href="{{ url_for('auth.resend_verification') }}">Resend</a>
</p>

{% endif %}
```

Add some CSS to make it a little better spaced:


Now let's create a route thats a little more informative for the user, which will pave the way for us to properly resend once our get user function works with tokens (right now it uses firebase admin sdk to look up UID, which doesn't respond with a token - a relic of how we connect with both pyrebase and firebase sdk).

That would be this code here in the auth/routes.py file.
```
@bp.route('/resend_verification', methods=['GET'])
def resend_verification():
    flash('Sign in again to resend verification email', 'orange')
    
    return redirect(url_for('auth.sign_in'))
```

Then just change the url_for code in the base.html template.

`url_for('auth.resend_verification')`


We're good to go!

Next we need to make it so users can view and update their profiles.

In the auth/routes.py we should add this.

```
@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('auth/profile.html')
```

Now add a template for the route to show.
```
{% extends "main/base.html" %}

{% block content %}
<h3>Profile</h3>
<p>Your user profile information.</p>

<div class="row">
    <div class="col s12 m5">
        <div class="card-panel">
            <p>{{ current_user.id }}</p>
            <p>{{ current_user.name }}</p>
            <p>{{ current_user.email }}</p>
            <p>{{ current_user.verified }}</p>
        </div>
    </div>
</div>
{% endblock %}
```

We need to adjust the base template so the nav has a link in there too.

`<li id="auth-profile"><a href="{{ url_for('auth.profile') }}">Profile</a></li>`


While we're in the base template, let's fix the active navs since we moved to the new blueprint structure. We can't use '.' in the css id so we have to change them to '-' instead.

```
<script>
    $(document).ready(function () {
        var endpoint = "#{{request.endpoint}}".replace(/\./g, "-");
        $(endpoint).addClass("active");
        $(".dropdown-trigger").dropdown();
    })
</script> 
```

Then we just change anywhere it says `<li id="sign_up">` or similar to ` <li id="auth-sign_up">`.

Ok so let's improve our profile page by making it a table with labels.

```
<table>
    <tbody>
        <tr>
            <td>ID</td>
            <td>{{ current_user.id }}</td>
        </tr>
        <tr>
            <td>Name</td>
            <td>{{ current_user.name }}</td>
        </tr>
        <tr>
            <td>Email</td>
            <td>{{ current_user.email }}</td>
        </tr>
        <tr>
            <td>Verified?</td>
            <td>{{ current_user.verified }}</td>
        </tr>                   
    </tbody>
</table>
```

Great, now let's make it possible to update the username, email, etc, as well as reset the password.

The User model needs a new method which changes the email if that's what changes, or just the name if so. We separate them becase we want to be able to make the user no longer verified if they change the email.

```
def edit(self, name, email):
    #email change
    if self.email != email:
        auth.update_user(
            self.id,
            email=email,
            display_name=name,
            email_verified=False,
        )
        self.verified = False
        self.name = name
        self.email = email

    #just a name change
    else:
        auth.update_user(
            self.id,
            display_name=name,
        )
        self.name = name
```

Then the form looks like this:
```

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('UPDATE')

```


We should also update the auth/routes.py
```
@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data

        #authenticate a user
        try:
            current_user.edit(name, email)

            # Update successful
            flash('User {}, updated with email={} and name={}'.format(
                 current_user.id, current_user.email, current_user.name
                 ), 'teal')

            return redirect(url_for('auth.profile'))

        except Exception as e:
            # Update unsuccessful
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            flash("Error: {}".format(error), 'red')

    form.name.data = current_user.name
    form.email.data = current_user.email
        
    return render_template('auth/edit_profile.html', title='Edit Profile', form=form)
```

This basically auto-fills the form with existing values, then also posts the changes if made.

```
{% extends "main/base.html" %}

{% block content %}
<h3>Edit Profile</h3>
<p>Update your profile email or name.</p>

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
                <p class="right-align">
                    <button type="submit" name="btn" class="waves-effect waves-light btn blue">
                    UPDATE
                    </button>
                </p>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

Now let's add some more meta data to users, namely their job title.

To do this we need to connect to the db. We also don't want this to happen on every call, because it means double the amount of traffic to firebase, so let's just do this in a separate get_meta function.

First update the User model with two methods
```
def get_meta(self):
    meta = db.child('users').child(self.id).val()
    return meta

def set_meta(self, job_title):
    db.child('users').child(self.id).set({
        "job_title": job_title
    })
```

Add this line to the edit user method

`self.set_meta(job_title)`

Now add this line to the form
`job_title = StringField('Job title')`

We don't want to make it required, in case it's blank (which will be the default for new users).

In the profile/edit route, add this line on validate
`job_title = form.job_title.data`

As well as updating the 'current_user.edit' function
`current_user.edit(name, email, job_title)`

Also the form prefill section
```
meta = current_user.get_meta()
if meta:
    form.job_title.data = meta['job_title']
```

Also add this to the edit_profile template.
```
<p class="input-field">
    {{ form.job_title.label }}<br>
    {{ form.job_title(size=32, class_="validate") }}<br>
    {% for error in form.job_title.errors %}
    <span class="helper-text" data-error="[{{ error }}]" data-success=""></span>
    {% endfor %}
</p>
```

The profile view too.
```
<tr>
    <td>Job Title</td>
    <td>{{ meta.job_title }}</td>
</tr>
```

You need to pass the meta variable to the profile view.
```
@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    meta = current_user.get_meta()
    return render_template('auth/profile.html',  title='View Profile', meta=meta)
```

We also want to add metadata for when the user was created. So add this to the User.get method.
`created=firebase_user.user_metadata.creation_timestamp`

Also add it to the User.create function, as well as the auth, which users Pyrebase.

`created=pyr_user_info['users'][0]['createdAt']`

Add it to the init
```
 def __init__(self, uid, email, name, verified, created):
    self.id = uid
    self.email = email
    self.name = name
    self.verified = verified
    self.created = created
```

Cool now let's add the timestamp to the profile page.

```
<tr>
    <td>Created</td>
    <td class="grey-text">{{ current_user.created }}</td>
</tr>
```

But let's format this a bit better in the routes.

add at the top `from datetime import datetime`

then
```
@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    meta = current_user.get_meta()
    timestamp = current_user.created
    created_date = datetime.fromtimestamp(timestamp / 1000)
    format_date = created_date.strftime("%b %d %Y %H:%M:%S")

    return render_template('auth/profile.html',  title='View Profile', meta=meta,
        created_date=format_date)
```

Then update created date in the template
`<td class="grey-text">{{ created_date }}</td>`

Let's also add profile pictures. This is a bigger job and we want it relatively self-contained, so let's make it in a separate form.

First let's create the route. It needs to be a form for a get request, as well as post the photo too. 

```
@bp.route('/profile/upload', methods=['GET', 'POST'])
@login_required
def upload_photo():
    form = UploadPhotoForm()

    if form.validate_on_submit():
        photo = form.photo.data

        #upload an image
        try:
            photo_url = current_user.upload(photo)

            # Update successful
            flash('User {}, updated photo={}'.format(current_user.id, photo_url), 'teal')
            return redirect(url_for('auth.profile'))

        except Exception as e:
            # Update unsuccessful
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            flash("Error: {}".format(error), 'red')
        
    return render_template('auth/upload_photo.html', title='Upload Photo', form=form)
```

To grab the photo it's basically the same as any form field, and then we pass it to a function on the user called upload, which we'll write next.

In auth/models.py add the photo_url to the __init__ method.

```
def __init__(self, uid, email, name, verified, created, photo_url):
        self.id = uid
        self.email = email
        self.name = name
        self.verified = verified
        self.created = created
        self.photo_url = photo_url
```

You also need to add it to the get, create and auth method.

`photo_url=firebase_user.photo_url`

Now to add the upload method.

```
def upload(self, photo):

        temp = tempfile.NamedTemporaryFile(delete=False)

        # Save temp image
        photo.save(temp.name)

        pyr_store.child('profiles/{}/{}'.format(self.id, temp.name)).put(temp.name)

        photo_url = pyr_store.child('profiles/{}/{}'.format(self.id, temp.name)).get_url(None)

        auth.update_user(
            self.id,
            photo_url=photo_url
        )
        self.photo_url = photo_url

        # Clean-up temp image
        temp.close()
        os.remove(temp.name)

        return photo_url
```

This uses a library to make temporary files (for when you're saving the photo locally before uploading) as well as the pyr_store object that we use to upload to google cloud storage from pyrbase. So make sure your libraries look like this:

```
from flask_login import UserMixin
from app import pyr_auth, pyr_store, db
from firebase_admin import auth
from flask_login import login_user, logout_user
import os
import tempfile
```

To import pyr_store you have to do this in the app/__init__.py file.
`pyr_store = firebase.storage()`

The form you add to auth/forms.py is pretty simple:
```
class UploadPhotoForm(FlaskForm):
    photo = FileField('image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('UPLOAD')
```

This is what the HTML looks like for the form. It goes in templates/auth and looks similar to the other form html fields.

The difference in this case is to get the styling right we had to do a bit more with the form field divs.

```
{% extends "main/base.html" %}

{% block content %}
<h3>Upload Photo</h3>
<p>Upload a new profile photo.</p>

<div class="row">
    <div class="col s12 m5">
        <div class="card-panel">
            <form action="" method="post" enctype="multipart/form-data">
                {{ form.hidden_tag() }}

                <div class="file-field input-field">
                    <div class="btn">
                        <span>SELECT</span>
                        {{ form.photo() }}
                    </div>
                    <div class="file-path-wrapper">
                        <input class="file-path validate" type="text">
                    </div>
                    {% for error in form.photo.errors %}
                    <span class="helper-text" data-error="[{{ error }}]" data-success=""></span>
                    {% endfor %}
                </div>

                <p class="right-align">
                    <button type="submit" name="btn" class="waves-effect waves-light btn blue">
                    UPLOAD
                    </button>
                </p>
            </form>
        </div>
        <a href="{{ url_for('auth.profile') }}">< Back to Profile</a>
    </div>
</div>
{% endblock %}
```


Now finally let's edit the profile page so there's a path to this route.

This is the specific code for the photo:
```
<tr>
    <td>Photo</td>
    <td class="col s6">
        <div class="row center-align" style="margin-bottom: 0px;">
            {% if current_user.photo_url %}
            <img src="{{ current_user.photo_url }}" class="circle responsive-img">
            {% else %}
            <img src="https://via.placeholder.com/150" class="circle responsive-img">
            {% endif %}
        </div>
        <div class="row center-align">
            <a href="{{ url_for('auth.upload_photo') }}">Upload</a>
        </div>
    </td>
</tr>
```

Though I made a lot of style edits to the page, so here's the full code:
```
{% extends "main/base.html" %}

{% block content %}
<h3>Profile</h3>
<p>Your user profile information.</p>

<div class="row">
    <div class="col s12 m8 l7">
        <div class="card-panel">
            <table>
                <tbody>
                    <tr>
                        <td>Photo</td>
                        <td class="col s6">
                            <div class="row center-align" style="margin-bottom: 0px;">
                                {% if current_user.photo_url %}
                                <img src="{{ current_user.photo_url }}" class="circle responsive-img">
                                {% else %}
                                <img src="https://via.placeholder.com/150" class="circle responsive-img">
                                {% endif %}
                            </div>
                            <div class="row center-align">
                                <a href="{{ url_for('auth.upload_photo') }}">Upload</a>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>ID</td>
                        <td class="grey-text">{{ current_user.id }}</td>
                    </tr>
                    <tr>
                        <td>Created</td>
                        <td class="grey-text">{{ created_date }}</td>
                    </tr>
                    <tr>
                        <td>Name</td>
                        <td>{{ current_user.name }}</td>
                    </tr>
                    <tr>
                        <td>Email</td>
                        <td>{{ current_user.email }}</td>
                    </tr>
                    <tr>
                        <td>Verified</td>
                        {% if not current_user.verified %} 
                        <td class="red-text">{{ current_user.verified }}
                            &nbsp; 
                            <a href="{{ url_for('auth.resend_verification') }}">Resend</a>
                        </td>
                        {% else %}
                        <td class="grey-text">{{ current_user.verified }}</td>
                        {% endif %}
                    </tr>
                    <tr>
                        <td>Password</td>
                        <td>
                            &#x2022;&#x2022;&#x2022;&#x2022;&#x2022;&#x2022;&#x2022;&#x2022;&#x2022;&#x2022;&#x2022;&#x2022;
                            &nbsp;
                            <a href="{{ url_for('auth.reset_password') }}">Reset</a>
                        </td>
                    </tr>
                    <tr>
                        <td>Job Title</td>
                        <td>{{ meta.job_title }}</td>
                    </tr>                   
                </tbody>
            </table>
            <p class="right-align">
                <a href="{{ url_for('auth.edit_profile') }}">
                    <button type="submit" name="btn" class="waves-effect waves-light btn blue">
                        EDIT
                    </button>
                </a>
            </p>
        </div>
    </div>
</div>
{% endblock %}
```

Ok just for fun let's add gravatars. This let's us pull the users picture if they uploaded it at some point for wordpress or other services that use gravatar. 

This is from this tutorial: [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars)

This will be entirely handled in the User model on account creation, and will serve as a default until they change their profile pic.

Add this to the top of the /auth/models.py page.
`from hashlib import md5`

Add this method to the User model
```
def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
```

The identicon part gives you a unique image based on the hash of your URL, if no photo is found.

Now we can call the photo url pretty easily like this:
`user.avatar(128)`

We won't actually upload it in our system, no need to store all those extra images. Instead let's just call it when there's no profile photo.

In the profile.html template theres this part.

```
{% if current_user.photo_url %}
<img src="{{ current_user.photo_url }}" class="circle responsive-img">
{% else %}
<img src="https://via.placeholder.com/150" class="circle responsive-img">
{% endif %}

```

We just need to change the second img if no current_user.photo_url to this.

`<img src="{{ current_user.avatar(128) }}" class="circle responsive-img">`

We could also bake this into the account creation and store it in firebase if we like, but we won't bother with this right now.
