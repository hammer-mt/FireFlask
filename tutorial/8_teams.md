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




