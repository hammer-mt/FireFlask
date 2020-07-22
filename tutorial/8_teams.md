### 8: Adding Teams and Roles

We now want to add the ability to create a team and invite coworkers or colleagues to that team.

We'll use this blog post as a guide:
[https://blog.checklyhq.com/building-a-multi-tenant-saas-data-model/](https://blog.checklyhq.com/building-a-multi-tenant-saas-data-model/)

Also interesting are these posts:
- [https://stackoverflow.com/questions/2748825/what-is-the-recommended-approach-towards-multi-tenant-databases-in-mongodb](https://stackoverflow.com/questions/2748825/what-is-the-recommended-approach-towards-multi-tenant-databases-in-mongodb)
- [https://usersnap.com/blog/cloud-based-saas-architecture-fundamentals/](https://usersnap.com/blog/cloud-based-saas-architecture-fundamentals/)
- [https://www.indiehackers.com/post/ror-saas-boilerplate-app-market-need-fb7af3d8db](https://www.indiehackers.com/post/ror-saas-boilerplate-app-market-need-fb7af3d8db)

Here's the general data structure of what we want eventually:

- Users can create many Teams.
- Teams can have many Users.
- Users have role-based access to a Team.
- Teams each have their own collection.

Teams
- id
- name
- current_period_ends
- stripe_subscription_id
- stripe_customer_id
- plan
- features []
- max_users

Memberships
- id
- user_id
- team_id
- role ['READ', 'EDIT', 'ADMIN', 'OWNER']
- receive_weekly_updates

Then of course our Users db is already taken care of by Firebase. We'll use the firebase uid as the user_id. Note a lot of these things aren't really needed right now, for example max users, features, stripe ids or receive weekly updates. We only included them to show what it will become eventually.

For now let's start with a simpler model that just gives us what we immediately need.

Teams
- id
- name

Memberships
- id
- user_id
- team_id
- role ['READ', 'EDIT', 'ADMIN', 'OWNER']

Memberships are the relationship between users and teams - this allows us to query for all the teams a user is part of, or all the users for a team.

One small bit of refactoring first.

In app let's change db to pyr_db so we know it comes from firebase. Also update it wherever db is referenced in auth/models.py

Now let's make the Team class in auth/models.py

```
class Team():
    def __init__(self, id_, name):
        self.id = id_
        self.name = name
    
    @staticmethod
    def get(team_id):
        team = pyr_db.child('teams').child(team_id).get().val()
        return team

    @staticmethod
    def create(name):
        team_res = pyr_db.child('teams').push({
            "name": name
        })
        team_id = team_res['name'] # api sends id back as 'name'
        print('Sucessfully created new team: {0}'.format(team_id))

        return team_id

    def update(self, name):
        pyr_db.child('teams').child(self.id).update({
            "name": name
        })
```

We have the basic name and id, as well as the ability to create or update teams.

Let's create a form for users to create new teams so we can test this out in auth/routes.py

```
class TeamForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('SUBMIT')
```

Now let's make a html page for adding teams. We can mostly copy the edit profile template.

```
{% extends "main/base.html" %}

{% block content %}
<h3>Add Team</h3>
<p>Create a new team for your company.</p>

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
                <p class="right-align">
                    <button type="submit" name="btn" class="waves-effect waves-light btn blue">
                    ADD TEAM
                    </button>
                </p>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

For the routes we can copy the update profiles as an example. Make sure to import the new Team model and forms at the top.

```
@bp.route('/add_team', methods=['GET', 'POST'])
@login_required
def add_team():
    form = TeamForm()

    if form.validate_on_submit():
        name = form.name.data

        #create a team
        try:
            team_id = Team.create(name)
            team = Team.get(team_id)

            # Update successful
            flash('Team id={}, created with name={}'.format(team_id, team['name']), 'teal')
            return redirect(url_for('auth.add_team'))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')
        
    return render_template('auth/add_team.html', title='Add Team', form=form)
```

This is a pattern that should be familiar by now - try and create, if it fails, print the error.

You should be able to add teams and they show up in firebase.

Now let's add the page where we can see the team we just created.

```
{% extends "main/base.html" %}

{% block content %}
<h3>Team</h3>
<p>Your team profile information.</p>

<div class="row">
    <div class="col s12 m8 l7">
        <div class="card-panel">
            <table>
                <tbody>
                    <tr>
                        <td>ID</td>
                        <td class="grey-text">{{ team_id }}</td>
                    </tr>
                    <tr>
                        <td>Name</td>
                        <td>{{ team.name }}</td>
                    </tr>                
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

Here's the route.
```
@bp.route('/teams/<team_id>', methods=['GET'])
@login_required
def view_team(team_id):
    team = Team.get(team_id)
    title = 'View Team {}'.format(team['name'])
        
    return render_template('auth/view_team.html', title=title, team=team)
```

Next let's make it so you can update the name of the team.
```
{% extends "main/base.html" %}

{% block content %}
<h3>Edit Team</h3>
<p>Update your team name.</p>

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
                <p class="right-align">
                    <button type="submit" name="btn" class="waves-effect waves-light btn blue">
                    UPDATE
                    </button>
                </p>
            </form>
        </div>
        <a href="{{ url_for('auth.profile', team_id=team_id) }}">< Back to Team</a>
    </div>
</div>
{% endblock %}
```

Note: change the name of profile to view_profile to be consistent.

Let's add an edit button to the view of the team. Goes below the table.

```
<p class="right-align">
    <a href="{{ url_for('auth.edit_team', team_id=team_id) }}">
        <button type="submit" name="btn" class="waves-effect waves-light btn blue">
            EDIT
        </button>
    </a>
</p>
```

Now create this edit route.

```

@bp.route('/teams/<team_id>/edit', methods=['GET', 'POST'])
# @login_required
def edit_team(team_id):
    form = TeamForm()

    team = Team.get(team_id)

    if form.validate_on_submit():
        name = form.name.data

        #edit a team
        try:
            team.update(name)
            team = Team.get(team_id)

            # Update successful
            flash('Team {}, updated with name={}'.format(
                 team_id, team['name']), 'teal')

            return redirect(url_for('auth.view_team', team_id=team_id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')

    form.name.data = team['name']
        
    return render_template('auth/edit_team.html', title='Edit Team', form=form, 
        team_id=team_id, team=team)
```

Now we need to fix the models actually to make edits work. In our User model it worked well because we initialized a model before we sent it. We need to do the same here.

The new teams class looks like this:

```
class Team():
    def __init__(self, id_, name):
        self.id = id_
        self.name = name
    
    @staticmethod
    def get(team_id):
        team_data = pyr_db.child('teams').child(team_id).get().val()
        team = Team(
            id_=team_id, 
            name=team_data['name']
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

    def update(self, name):
        pyr_db.child('teams').child(self.id).update({
            "name": name
        })

        self.name = name
```

Remember to update the templates to use team.id instead of team_id.



The routes now will look like this - a little more simplified.

```

@bp.route('/add_team', methods=['GET', 'POST'])
# @login_required
def add_team():
    form = TeamForm()

    if form.validate_on_submit():
        name = form.name.data

        #create a team
        try:
            team = Team.create(name)

            # Update successful
            flash('Team id={}, created with name={}'.format(team.id, team.name), 'teal')
            return redirect(url_for('auth.view_team', team_id=team.id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')
        
    return render_template('auth/add_team.html', title='Add Team', form=form)


@bp.route('/teams/<team_id>', methods=['GET'])
# @login_required
def view_team(team_id):
    team = Team.get(team_id)
    title = 'View Team {}'.format(team.name)
        
    return render_template('auth/view_team.html', title=title, team=team)


@bp.route('/teams/<team_id>/edit', methods=['GET', 'POST'])
# @login_required
def edit_team(team_id):
    form = TeamForm()

    team = Team.get(team_id)

    if form.validate_on_submit():
        name = form.name.data

        #edit a team
        try:
            team.update(name)

            # Update successful
            flash('Team {}, updated with name={}'.format(
                 team.id, team.name), 'teal')

            return redirect(url_for('auth.view_team', team_id=team.id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')

    form.name.data = team.name
        
    return render_template('auth/edit_team.html', title='Edit Team', form=form, 
        team=team)
```

Now we can create teams, we need to associate them with users and vice versa.

So let's create the model for memberships in auth/models.py


```
class Membership():
    def __init__(self, id_, user_id, team_id, role):
        self.id = id_
        self.user_id = user_id
        self.team_id = team_id
        self.role = role
    
    @staticmethod
    def get(membership_id):
        membership_data = pyr_db.child('memberships').child(membership_id).get().val()
        membership = Membership(
            id_=membership_id, 
            user_id=membership_data['user_id'],
            team_id=membership_data['team_id'],
            role=membership_data['role']
        )
        return membership

    @staticmethod
    def create(user_id, team_id, role):
        membership_res = pyr_db.child('memberships').push({
            "user_id": user_id,
            "team_id": team_id,
            "role": role
        })
        membership_id = membership_res['name'] # api sends id back as 'name'
        print('Sucessfully created membership: {0}'.format(membership_id))

        membership = Membership.get(membership_id)
        return membership

    def update(self, role):
        pyr_db.child('memberships').child(self.id).update({
            "role": role
        })

        self.role = role
```

This is not too dissimilar from what we just did to create the teams model.

Let's also add a form to invite users to a team.

Make sure you import SelectField at the top.

Then the form looks like this:

```
class InviteForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    
    available_roles = ['READ', 'EDIT', 'ADMIN', 'OWNER']
    role_choices = [(role, role) for role in available_roles] # format required by flask wtf

    role = SelectField('Role', choices=role_choices, default='READ', validators=[DataRequired()])
    
    submit = SubmitField('INVITE')
```

We're providing an email because the user won't know the user id. So we need a method on user now to look up by email.

```
@staticmethod
def get_by_email(email):
    try:
        firebase_user = auth.get_user_by_email(email)

        print('Successfully fetched user data: {0}'.format(firebase_user.uid))
        flask_user = User(
            uid=firebase_user.uid,
            email=firebase_user.email,
            name=firebase_user.display_name,
            verified=firebase_user.email_verified,
            created=firebase_user.user_metadata.creation_timestamp,
            photo_url=firebase_user.photo_url
        )
        return flask_user
        
    except Exception as e:
        print(e)
        return None
```

Ok like before let's create a page where we can add memberships.

```
{% extends "main/base.html" %}

{% block content %}
<h3>Invite User</h3>
<p>Add a new user to your team.</p>

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
                <p class="input-field">
                    {{ form.role.label }}<br>
                    {{ form.role(size=32, class_="validate") }}<br>
                    {% for error in form.role.errors %}
                    <span class="helper-text" data-error="[{{ error }}]" data-success=""></span>
                    {% endfor %}
                </p>
                <p class="right-align">
                    <button type="submit" name="btn" class="waves-effect waves-light btn blue">
                    INVITE
                    </button>
                </p>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

Now in routes, add InviteForm to the top of the page as well as the Membership model.


Add this static method to the User model so we can invite users without logging them in.

```
@staticmethod
def invite(email):
    temp_pass = md5(email.lower().encode('utf-8')).hexdigest()

    # invite and send password reset
    pyr_user = pyr_auth.create_user_with_email_and_password(email, temp_pass)
    pyr_auth.send_password_reset_email(email)

    pyr_user_info = pyr_auth.get_account_info(pyr_user['idToken'])

    print(pyr_user)
    print(pyr_user_info)

    flask_user = User(
        uid=pyr_user['localId'],
        email=pyr_user['email'],
        name="",
        verified=False,
        created=pyr_user_info['users'][0]['createdAt'],
        photo_url=""
    )
    return flask_user
```

Now this is what the route looks like.

```
@bp.route('/teams/<team_id>/invite', methods=['GET', 'POST'])
@login_required
def invite_user(team_id):
    form = InviteForm()

    team = Team.get(team_id)

    if form.validate_on_submit():
        email = form.email.data
        role = form.role.data

        #create a team
        try:
            user = User.get_by_email(email)

            if not user:
                user = User.invite(email)
                
            membership = Membership.create(user.id, team_id, role)

            # Update successful
            flash('User {} added to team {} with role {}'.format(membership.user_id, membership.team_id,  membership.role), 'teal')
            return redirect(url_for('auth.view_team', team_id=team.id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')
        
    return render_template('auth/invite_user.html', title='Invite User', form=form, team=team)
```

Let's add links to and from the team page and invite page.

`<a href="{{ url_for('auth.view_team', team_id=team_id) }}">< Back to Team</a>`

`<a href="{{ url_for('auth.invite_user', team_id=team.id) }}">Invite users</a>`

One thing I forgot - to get select fields working you have to use materialize CSS to do this:

`$('select').formSelect();`

Put that in the base template in the document ready part of the scripts.

also in routes switch any team_ids converted over to `team = Team.get(team_id)`

So the process is:
- visit all teams page for user
- visit team page
- click invite
- enter email and role
- look up user by email
- if no user, create user with placeholder password
- reset user password so they get an alert
- create membership between user_id and team_id
- load page for that team's users, with new user present

We've built the ability to add memberships / invite users, but we haven't created the all teams page, or the users per team page.

First let's update the memberships model. This part is pretty straightforward.

```
@staticmethod
def get_users_by_team(team_id):
    users_by_team = pyr_db.child("memberships").order_by_child("team_id").equal_to(team_id).get()

    return users_by_team

@staticmethod
def get_teams_by_user(user_id):
    teams_by_user = pyr_db.child("memberships").order_by_child("user_id").equal_to(user_id).get()

    return teams_by_user
```

Now let's update the route for viewing a team, to see all the users on that team.

```
@bp.route('/teams/<team_id>', methods=['GET'])
@login_required
def view_team(team_id):
    team = Team.get(team_id)
    users_by_team = Membership.get_users_by_team(team_id)
    team_members = []
    for membership in users_by_team:
        membership_data = membership.val()
        user = User.get(membership_data['user_id'])

        member = {
            "name": user.name,
            "role": membership_data['role'],
        }
        team_members.append(member)

    title = 'View Team {}'.format(team.name)
        
    return render_template('auth/view_team.html', title=title, team=team, team_members=team_members)
```

P.S. one great trick to stop having to log in all the time, is to just comment out @login_required while you're working on it.

So for example with getting all teams you would do the following:
```
@bp.route('/teams', methods=['GET'])
# @login_required
def list_teams():
    teams_by_user = Membership.get_teams_by_user(current_user.id)

    teams_list = []
    for membership in teams_by_user:
        membership_data = membership.val()
        team_data = Team.get(membership_data['team_id'])

        team = {
            "id": team_data.id,
            "name": team_data.name,
            "role": membership_data['role'],
        }
        teams_list.append(team)

    return render_template('auth/list_teams.html', title='Teams', teams_list=teams_list)
```

Test it out and then uncomment the login_required.

Now let's update the template for teams.

```
<div class="row">
    <div class="col s4">
        <h5>Team members</h5>
    </div>
</div>
<div class="row">
    
    {% for member in team_members %}
    <div class="col s2">
        <div class="card-panel">
            <p>Name: {{ member.name }}</p>
            <p>Role: {{ member.role }}</p>
        </div>

    </div>
    
    {% endfor %}
</div>
<div class="row">
    <div class="col s2">
        <a href="{{ url_for('auth.invite_user', team_id=team.id) }}">
            <button type="submit" name="btn" class="waves-effect waves-light btn red">
                INVITE
            </button>
        </a>
    </div>
</div>
```

This goes underneath the card panel.

Also we should add the template for all teams listing.

```
{% extends "main/base.html" %}

{% block content %}
<h3>Teams</h3>
<p>A list of all of the teams you have access to.</p>

<div class="row">
    <a href="{{ url_for('auth.add_team') }}">
        <button type="submit" name="btn" class="waves-effect waves-light btn red">
            ADD
        </button>
    </a>

</div>


<div class="row">
    
    {% for team in teams_list %}
    <div class="col s2">
        <a href="{{ url_for('auth.view_team', team_id=team.id) }}">
            <div class="card">
                <div class="card-content center-align">
                    <span class="card-title">{{ team.name }}</span>
                </div>
                <div class="card-action">
                    <div class="right-align">{{ team.role }}</div>
                </div>
            </div>
        </a>

    </div>
    
    {% endfor %}
</div>


{% endblock %}

```

Then add a link in the nav bar.
`<li id="auth-list_teams"><a href="{{ url_for('auth.list_teams') }}">Teams</a></li>`

Once you do this and test it out, you'll run into an indexing issue. To solve that just change your rules to this in the firebase realtime database.

```
{
  /* Visit https://firebase.google.com/docs/database/security to learn more about security rules. */
  "rules": {
    ".read": false,
    ".write": false,
    "memberships": {
      ".indexOn": ["team_id", "user_id"]
    }
  }
}
```

Memberships should be working now! But any user can invite any other user, the roles and memberships don't do anything to stop them.

First let's add a user as the owner when they create a team, and remove that option from the dropdown in the invite form (we'll add the ability to change owners when we build an admin panel)

`Membership.create(current_user.id, team.id, "OWNER")`

This goes in the add_team route.

Ok so let's now remove the ability to see a team if the user isn't in that team.

In view team it's straightforward to check because we already have a list of team members. So we just do this.

Initialize 'authorized' as false
`authorized = False`

Then add this in the loop
```
if current_user.id == user.id:
    authorized = True
```

Then put in an abort
```
if not authorized:
    abort(401, "You don't have access to that team")
```

Let's also add in a role, param, so it ends up like this:
```
@bp.route('/teams/<team_id>', methods=['GET'])
@login_required
def view_team(team_id):
    team = Team.get(team_id)
    users_by_team = Membership.get_users_by_team(team_id)

    team_members = []
    authorized = False
    role = False
    for membership in users_by_team:
        membership_data = membership.val()
        user = User.get(membership_data['user_id'])

        member = {
            "id": user.id,
            "name": user.name,
            "role": membership_data['role'],
        }
        team_members.append(member)

        if current_user.id == user.id:
            authorized = True
            role = membership_data['role']

    if not authorized:
        abort(401, "You don't have access to that team")

    title = 'View Team {}'.format(team.name)
        
    return render_template('auth/view_team.html', title=title, team=team, team_members=team_members, role=role)
```

Remember to remove the edit button if they aren't the right role.

```
{% if role in ['ADMIN', 'OWNER'] %}
<p>
    <a href="{{ url_for('auth.edit_team', team_id=team.id) }}">
        <button type="submit" name="btn" class="waves-effect waves-light btn blue">
            EDIT
        </button>
    </a>
</p>
{% endif %}
```

However we will probably want to check the user's role and authorized status in a bunch of places in future, so let's make a function for that as part of memberships.

```
@staticmethod
def user_role(user_id, team_id):
    users_by_team = pyr_db.child("memberships").order_by_child("team_id").equal_to(team_id).get()

    role = None
    for membership in users_by_team:
        membership_data = membership.val()

        if membership_data['user_id'] == user_id:
            role = membership_data.role
    
    return role
```

Let's use this in the team edit route.

```
role = Membership.user_role(current_user.id, team_id)
if role not in ["ADMIN", "OWNER"]:
    abort(401, "You don't have access to edit this team.")
```

Do this for invite too.

We should also put some protection in now to stop people adding the same user twice to the same team.

```
@staticmethod
def create(user_id, team_id, role):
    existing_role = Membership.user_role(user_id, team_id)

    if existing_role:
        raise Exception("User already has access")
    else:
        membership_res = pyr_db.child('memberships').push({
            "user_id": user_id,
            "team_id": team_id,
            "role": role
        })
        membership_id = membership_res['name'] # api sends id back as 'name'
        print('Sucessfully created membership: {0}'.format(membership_id))

        membership = Membership.get(membership_id)
        return membership
```

One more thing, let's make it possible for owners and admins to delete a membership, or remove a user from a team. We should also stop people deleting the owner so there's always one person on a team.

Let's create the route first.

```
@bp.route('/<membership_id>/delete', methods=['GET', 'POST'])
@login_required
def remove_user(membership_id):

    membership = Membership.get(membership_id)

    role = Membership.user_role(current_user.id, membership.team_id)
    if role not in ["ADMIN", "OWNER"]:
        abort(401, "You don't have access to remove this user.")
    elif membership.role == "OWNER":
        abort(401, "You cannot remove the owner of the account.")
    else:
        membership.remove()

        flash('User {} removed from team {}'.format(membership.user_id, membership.team_id), 'teal')
        return redirect(url_for('auth.view_team', team_id=membership.team_id))
    
```

This will check the person has the authority to remove. It will also check if the membership role is a OWNER.

Then it will remove.

Now we need to make that remove method in Membership model.

```
def remove(self):
    pyr_db.child('memberships').child(self.id).remove()
```

Now in the view team we just need to add the remove option.

```
{% for member in team_members %}
<div class="col s2">
    <div class="card-panel">
        <p>Name: {{ member.name }}</p>
        <p>Role: {{ member.role }}</p>
        {% if role in ['ADMIN', 'OWNER'] %}
        <a href="{{ url_for('auth.remove_user', membership_id=member.membership_id) }}">
            <button type="submit" name="btn" class="waves-effect waves-light btn red">
                REMOVE
            </button>
        </a>
        {% endif %}
    </div>

</div>

{% endfor %}
```



Ok so that's pretty much done! For cleanliness let's refactor so all of this is in a separate blueprint.