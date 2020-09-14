### 13: Creating a testing suite
In the early days of a project you probably just want to get on with building, and maybe you aren't even sure if your idea will work. As time goes on and complexity increases, it can become more difficult to make improvements without accidentally breaking something. This is where a well-implemented test suite can help – it can give you confidence in your code because you can run it after every change, and catch any bugs before you deploy. This is one of the main concepts that separates data scientists and software engineers – the closest we normally get to testing is running a cell in a Jupyter Notebook. When you have a tool in production though, it quickly becomes a good idea to learn!

We'll be piecing together our testing code from various resources across the web.
- [Testing Flask Applications](https://flask.palletsprojects.com/en/1.1.x/testing/)
- [Mocking External APIs in Python](https://realpython.com/testing-third-party-apis-with-mocks/)
- [Testing External APIs With Mock Servers](https://realpython.com/testing-third-party-apis-with-mock-servers/)
- [Unit Testing and Test-Driven Development in Python](https://www.linkedin.com/learning/unit-testing-and-test-driven-development-in-python)
- [The Flask Mega-Tutorial Part XV: A Better Application Structure](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure)
- [Examples and customization tricks](https://docs.pytest.org/en/latest/example/index.html)
- [The Minimum Viable Test Suite](https://realpython.com/the-minimum-viable-test-suite/)
- [The Difference Between Mocks and Stubs](https://martinfowler.com/articles/mocksArentStubs.html#TheDifferenceBetweenMocksAndStubs)
- [Signals](https://flask.palletsprojects.com/en/1.1.x/signals/)
- [Testing a Login Flow](https://developers.facebook.com/docs/facebook-login/testing-your-login-flow/)
- [Configuring Your Flask App](https://hackersandslackers.com/configure-flask-applications/)
- [Flask application factory pattern and testing](http://nidkil.me/2017/02/07/flask-application-factory-pattern/)
- [Testing our Hello World app](https://riptutorial.com/flask/example/4122/testing-our-hello-world-app)
- [Python Web Applications With Flask – Part III](https://realpython.com/python-web-applications-with-flask-part-iii/)
- [Flask Series: Testing](https://damyanon.net/post/flask-series-testing/)
- [Build and Test a Mini Flask Application](https://medium.com/better-programming/build-test-and-deploy-a-mini-flask-application-1d9ca6c45115)
- [Build, Test, and Deploy a Flask Application: Part 4](https://medium.com/better-programming/build-test-and-deploy-a-flask-application-part-4-5aa4f079fadb)
- [FUNCTION TEMPLATE](https://github.com/mjt145/function)
- [Testing a Flask Application using pytest](https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/)
- [Test a Flask App with Selenium WebDriver - Part 1](https://scotch.io/tutorials/test-a-flask-app-with-selenium-webdriver-part-1)
- [Packaging a python library](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)

#### Goals of testing
- Tests should run fast
    - So that they can be part of the development workflow
    - so they don't slow down your development or deploys
- Tests should produce consistent results
    - run twice, get the same failure or success
    - opposite of "flaky"
    - intermittent test failures are annoying, since it makes it harder to find what's going wrong
- Tests should find bugs, if they exist
    - 'Test Coverage' tells us how much of the code is run when we run the tests
    - But, it doesn't tell us about 'correctness' or about whether 'edge case' values are put through the function
    - Corollary: Tests should not fail for things that aren't bugs
- Tests should cover edge cases
    - The space of possible inputs is impossibly large, so we can't test everything
    - Instead, we try to reason through what combinations of inputs are worth checking
    - 'Edges' - 0, 1, large inputs, improper inputs
    - When we find actual bugs in production, we add test cases to catch those
    - "Regression" tests to prevent 'regressing' to the old, buggy state 
- Tests should make refactoring easier
    - Running the tests should make you confident that the code still works
    - Tests should avoid testing internal implementation details (since then the test would break when you refactored)
    - Choosing the boundaries around a test is _hard_

#### What to test
When we deployed FireFlask, we had a list of features and functionality to test manually. Let's see if we can get as close as possible to testing against that list, but this time programmatically.
- Visit the homepage
- Sign up and sign out
- Log in and edit your profile
- Create a team
- Add account id and conversion event to team
- Connect Facebook ads
- Invite a user to a team
- Log in as invited user
- Visit the generic dashboard
- Visit the Facebook dashboard

These may be primarily integration tests, as they describe multiple components working together at once to generate a user-visible behavior. We will also eventually want to run unit tests for each function in our project, so we know all our individual functions are working. We will need to test our google cloud functions somewhat differently to our main code. Finally let's also do some in-browser testing with Selenium, just for fun!

#### Creating tests
First let's create a folder to house our tests. It should be at the top level, same as the app folder, and be called 'tests'.

We want to install pytest
`pip install pytest`
`pip freeze > requirements.txt`

Then we just want to create a dummy test to check pytest is working. Create a file called `test_dummy.py` in the tests folder.

Then just add the following code to it:
```
import pytest

def test_dummy():
    assert True
```

Run pytest and it should show you one test ran and passed.
`pytest`

Great now we can delete that and move onto testing the main module in our app (where index is located). Create a file called `test_app.py`. This is where we'll test the app is working properly.

We also need to add a `__init__.py` file (this is blank) to the `tests` folder to make the import work.

Let's first just test the import works.

```
import pytest
from app import create_app

def test_app():
    assert True
```

Run pytest and you should see it passes. If something goes wrong it's likely to do with the file structure and imports, so go back and read through the instructions again.

Now let's modify the test file so we create a test client for flask, and can run our first planned text, loading the homepage.

To load the flask app we'll need to load the config variable, which we can do by adding this to the imports (this is the exact same way we load it in `app/__init__.py`).

`from config import Config`

Then we want to be able to modify this Config object for testing purposes, for example to tell Flask we're testing.

```
class TestConfig(Config):
    TESTING = True
```

This uses inheritance to still load everything from the previous Config, but we can add our own values.

Now we need to create a fixture, which will load our flask testing client for every test that needs it.

```
@pytest.fixture()
def tester():
    app = create_app(TestConfig)
    tester = app.test_client()
    yield tester
```

This now gives us a tester we can pass into our test which creates a test client version of flask.

```
def test_visit_the_homepage(tester): 
    response = tester.get('/')
    assert response.status_code == 200
    assert b'FireFlask' in response.data
```

This loads the tester flask client, calls the index (homepage), then asserts that the response code is 200 and the word 'FireFlask' is in the response data.

Run pytest and you should see it pass - that's our first test case done.

- ~~Visit the homepage~~
- Sign up and sign out
- Log in and edit your profile
- Create a team
- Add account id and conversion event to team
- Connect Facebook ads
- Invite a user to a team
- Log in as invited user
- Visit the generic dashboard
- Visit the Facebook dashboard

Next let's look into testing the user model for signup and signout. We want to put this in a separate file to make it easier to see what areas we're testing. So we need to do a bit of restructuring of our test file.

We want all our tests to have access to our fixture, and we don't want to have to import pytest every time, so we can put these into a `conftest.py` file.

```
import pytest
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True

@pytest.fixture()
def tester():
    app = create_app(TestConfig)
    tester = app.test_client()
    yield tester
```

Now all we need in our `test_app.py` file is that single test.
```
def test_visit_the_homepage(tester): 
    response = tester.get('/')
    assert response.status_code == 200
    assert b'FireFlask' in response.data
```

Now in the future if we wanted to do more generic app testing (like check the 404 page shows) we could add it here alongside this test.

Now let's create a new file called `test_auth.py`

This is where we're going to test sign up and sign out, as well as log in and edit your profile.

Normally we wouldn't want to include third party systems in our testing, as it might slow things down or incur costs. However for our purposes since we outsourced our authentication entirely to Firebase, it makes sense to test Firebase itself. 

Rather than messing around with an emulator which looks like a pain to configure, for now let's test the actual service so we can get going quicker and not have to make too many modifications to our code or config.

One thing we will need however is a way to delete users, as we don't want to leave a lot of new users in the admin system. So let's add that to our user model.

We won't yet offer this in our UI (the admin can delete users who request it) because we don't want to waste time thinking about the various implications (i.e. if the user is the only one on a team, do we also delete the team?).

```
def destroy(self):
        auth.delete_user(self.id)
        print(f"Deleted user {self.id}")
```

Rather than messing with the signup routes and finding a way to fake the form field, instead let's just test the User model directly.

We need to do a few things at once to make this possible, first we need to import the string and random modules to make a password for the fake test user, then import the User model.


```
import string
import random
from app.auth.models import User


def test_sign_up(tester):
    name = 'tester'
    email = 'test@example.com'
    password = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(7))
    print(name, email, password)
    user = User.create(name, email, password)
    assert user.email == email
    user.destroy()
```

The other thing we need to do is make environment variables available to pytest, because annoyingly they don't read from our yaml or flaskenv files.

So create a pytest.ini file at the top level of the application (i.e. same place as the flaskenv file) that looks like this:

```
[pytest]
env =
    FIREBASE_API_KEY=abcdefghijklmnopqrstuvwxyz
```

This will be what pyrebase reads from when making calls with an API key.

Finally we need to do some quick refactoring of our User model - right now it has login_user and logout_user which are session methods and shouldn't be included in our testing of the model right now.

In auth/model.py change the sign up and sign in methods.

```
@staticmethod
    def create(name, email, password):
        firebase_user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )
        print('Sucessfully created new user: {0}'.format(firebase_user.uid))

        # send verification
        pyr_user = pyr_auth.sign_in_with_email_and_password(email, password)
        pyr_auth.send_email_verification(pyr_user['idToken'])

        print("Sent email verification")

        flask_user = User(
            uid=firebase_user.uid,
            email=firebase_user.email,
            name=firebase_user.display_name,
            verified=firebase_user.email_verified,
            created=firebase_user.user_metadata.creation_timestamp,
            photo_url=firebase_user.photo_url
        )
        return flask_user

    @staticmethod
    def auth(email, password):
        pyr_user = pyr_auth.sign_in_with_email_and_password(email, password)
        pyr_user_info = pyr_auth.get_account_info(pyr_user['idToken'])

        is_verified = pyr_user_info['users'][0]['emailVerified']

        if not is_verified:
            # send verification
            pyr_auth.send_email_verification(pyr_user['idToken'])
            print("Sent email verification")

        firebase_user = auth.get_user(pyr_user['localId'])

        print('Sucessfully signed in user: {0}'.format(pyr_user['localId']))
        flask_user = User(
            uid=pyr_user['localId'],
            email=pyr_user['email'],
            name=pyr_user['displayName'],
            verified=is_verified,
            created=pyr_user_info['users'][0]['createdAt'],
            photo_url=firebase_user.photo_url
        )
        return flask_user
```

Also go in and delete the sign out method from User.

Then go to auth/routes.py to bring the login into the sign up and sign in methods there.

```
@bp.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        #authenticate the user
        try:
            user = User.auth(email, password)
            login_user(user, remember=True)

            # Sign in successful
            flash('User {}, logged in with id={}'.format(
                current_user.email, current_user.id), 'blue')
            return redirect(url_for('main.index'))

        except Exception as e:
            # Sign in unsuccessful
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            flash("Error: {}".format(error), 'red')
            
            return render_template('auth/sign_in.html', title='Sign In', form=form)
        
    return render_template('auth/sign_in.html', title='Sign In', form=form)

@bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        #authenticate a user
        try:
            user = User.create(name, email, password)
            login_user(user, remember=True)

            # Sign up successful
            flash('User {}, created with id={}'.format(
                current_user.email, current_user.id), 'teal')
            return redirect(url_for('main.index'))

        except Exception as e:
            # Sign up unsuccessful

            if type(e.args[0]) == str:
                 error = e.args[0] # weird bug where not returning json
            else:
                error_json = e.args[1]
                error = json.loads(error_json)['error']['message']
            flash("Error: {}".format(error), 'red')
        
    return render_template('auth/sign_up.html', title='Sign Up', form=form)

@bp.route('/sign_out', methods=['GET', 'POST'])
@login_required
def sign_out():
    user_id = current_user.id # save before user logged out
    logout_user()
    flash("User {} signed out".format(user_id), 'blue')
    return redirect(url_for("main.index"))
```

Now if you run pytest, it should work as planned.
`pytest -vv -s`

You'll see hopefully that the new user was created then destroyed.

Note it takes some time to run this now, so if you want to run the tests without auth, the command would be:
`pytest -vv -s -k "not _auth"`

Or if you only wanted to run auth tests it would be:
`pytest -vv -s -k "_auth"`

Now we're going to be creating a user for each new test, so let's put that into a fixture.

Move our imports across to conftest.
```
import string
import random
from app.auth.models import User
```

We need to first create a fixture for password (because we'll need to use this password when checking sign in methods later).

```
@pytest.fixture()
def password():
    password = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(7))
    yield password
```

Now we make a second fixture which takes this password in to create the user.

```
@pytest.fixture()
def user(password):
    name = 'tester'
    email = 'test@example.com'
    user = User.create(name, email, password)

    yield user

    print('')
    user.destroy()
```

Our sign up test can now be as simple as
```
def test_sign_up(user):
    assert user.email == 'test@example.com'
```

Now let's test sign in and see how we go.

First we'll need to remove this code from our sign in method in the User model (it was causing us to hit a rate limit).
```
if not is_verified:
    # send verification
    pyr_auth.send_email_verification(pyr_user['idToken'])
    print("Sent email verification")
```

Then the test should just be:
```
def test_sign_in(user, password):
    user = User.auth('test@example.com', password)
    assert user.email == 'test@example.com'
```

Now let's test editing a user's profile and see how that works.

```
def test_edit_profile(user):
    user.edit('tester 2', 'test_2@example.com', 'QA Tester')

    user = User.get(user.id)
    meta = user.get_meta()

    assert user.name == 'tester 2'
    assert user.email == 'test_2@example.com'
    assert meta.get('job_title') == 'QA Tester'
```

Ok so we've managed to cross off the first few things on our list. I know we haven't done logout, but then we're just using the plain flask implementation and as a new coder it probably won't be a good use of time to test components of a popular framework – instead we should focus on the parts we coded as that's where there is likely to be more mistakes! Obviously over time we should build up full test coverage, but on our first introduction to testing we should focus only on testing the most important parts or it'll get tedious.

- ~~Visit the homepage~~
- ~~Sign up~~ and sign out
- ~~Log in and edit your profile~~
- Create a team
- Add account id and conversion event to team
- Connect Facebook ads
- Invite a user to a team
- Log in as invited user
- Visit the generic dashboard
- Visit the Facebook dashboard

Next up is creating a team. Let's do that as the same time as adding an account id and conversion event, as well as inviting a user to team and loging in as that user. Then we'll finish up by testing the cloud functions for the generic dashboard and Facebook ads.

Let's create another file called `test_team.py`.

Just like on auth, we'll need to create the ability to remove a team and its memberships.

Each membership has it's own method for destroying (we use it when removing a user from a team) called Membership.remove(). Let's create something similar for Team.

```
def remove(self):
    pyr_db.child('teams').child(self.id).remove()
    print(f'Team {self.id} removed')
```

So first let's do our imports.

`from app.teams.models import Team, Membership`

Then also in conftest, create the fixture.

```
@pytest.fixture()
def team():
    name = 'Team Tester'
    team = Team.create(name)

    yield team
    
    print('')
    team.remove()
```

Then the test for team can be simply:
```
def test_create_team(team):
    assert team.name == 'Team Tester'
```

Now let's test updating the team and editing. Import the Team model (and Membership as we'll use it later)
`from app.teams.models import Team, Membership`

Then our team update testing is very similar to how we tested update users.

```
def test_update_team(team):
    team.update('Team Tester 2', '123456789', 'landing_page_view')

    team = Team.get(team.id)

    assert team.name == 'Team Tester 2'
    assert team.account_id == '123456789'
    assert team.conversion_event == 'landing_page_view'
```

Now let's test we can invite a user and let them log in.

First import user (so we can log in)
`from app.auth.models import User`

Then we need to create a new membership with our test user, and asset the user id, team id etc is correct. We'll then log the user in and see if that works, before removing the membership.

```
def test_membership_invite(team, user, password):
    role = "READ"
    membership = Membership.create(user.id, team.id, role)

    assert membership.user_id == user.id
    assert membership.team_id == team.id
    assert membership.role == role

    user = User.auth('test@example.com', password)
    assert user.email == 'test@example.com'

    print("")
    membership.remove()
```

There are obviously more comprehensive tests we can run on users and members, but for now this is good enough to move on to get test coverage on our cloud functions.

- ~~Visit the homepage~~
- ~~Sign up~~ and sign out
- ~~Log in and edit your profile~~
- ~~Create a team~~
- ~~Add account id and conversion event to team~~
- Connect Facebook ads
- ~~Invite a user to a team~~
- ~~Log in as invited user~~
- Visit the generic dashboard
- Visit the Facebook dashboard

Because of the way our application is built, the most important functionality always depends on cloud functions. So learning to test them is the key to most of the future testing we need to write. 

Yes we'll eventually want to write tests for all the smaller components of our login etc, but there won't be much innovation there, so we hopefully won't be as much at risk of it breaking as we would be with our functions.

First let's test our generic cloud `get_test_data` function, as that doesn't have any major needs with regards to connnecting to a third party API at all, and learning to test it will help us test the Facebook function. 

First let's get out of our environment and into the function environment.
`deactivate`
`functions\get_test_data_venv\Scripts\activate`

We need to add the environment variables to our pytest.ini (it doesn't matter what these variables are, this is just a test function it doesn't validate them).
```
    APP_ID=123456
    APP_SECRET=abcdef
```

Also make sure to pip install the following
`pip install pytest`
`pip install pytest-env`
`pip freeze > functions\get_test_data\requirements.txt`

We also have to add them to the environment for testing, then we can run the function to see how it works.
`$env:APP_ID="123456"`
`$env:APP_SECRET="abcdef"`
`python functions/get_test_data/main.py`

Then visit
`http://localhost:5000/?access_token=Mike&account_id=123456789&date_start=2020-01-01&date_end=2020-01-07`

And you should see the data. We programmed this to use a random seed so that the data is random, but always the same for the same call to the same parameters. So we should be able to test this properly. 

Grab the raw JSON response and save it somewhere to use later in your test.

Create a `test_get_test_data.py` file in your tests folder.

Add these imports:
```
import pytest
from functions.get_test_data.main import main
from flask import Flask, request
import json
```

Now create a tester client as a fixture to use.
```
@pytest.fixture()
def func_tester():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.route('/')(lambda: main(request))

    with app.app_context():
        func_tester = app.test_client()
        yield func_tester
```

Now we have what we need to write the test. First let's just check it comes back with a 200.

```
def test_get_test_data(func_tester):
    response = func_tester.get('/', query_string=dict(access_token="Mike", account_id="123456789", date_start="2020-01-01", date_end="2020-01-07"))
    assert response.status_code == 200
```

Then run 
`pytest -vv -k _get`

To see it (hopefully) working.

Next let's add our test case data from before and test it's working.

```
def test_get_test_data(func_tester):
    response = func_tester.get('/', query_string=dict(access_token="Mike", account_id="123456789", date_start="2020-01-01", date_end="2020-01-07"))
    assert response.status_code == 200
    test_data = [
        {
            "clicks": "6633.75", 
            "conversions": "804.09", 
            "date": "2020-01-01", 
            "impressions": "2043732.45", 
            "spend": "5360.61"
        }, 
        {
            "clicks": "8884.46", 
            "conversions": "1076.9", 
            "date": "2020-01-02", 
            "impressions": "2737130.16", 
            "spend": "7179.36"
        }, 
        {
            "clicks": "10416.11", 
            "conversions": "1262.56", 
            "date": "2020-01-03", 
            "impressions": "3209004.38", 
            "spend": "8417.06"
        }, 
        {
            "clicks": "11395.85", 
            "conversions": "1381.32", 
            "date": "2020-01-04", 
            "impressions": "3510843.23", 
            "spend": "9208.77"
        }, 
        {
            "clicks": "14497.23", 
            "conversions": "1757.24", 
            "date": "2020-01-05", 
            "impressions": "4466318.22", 
            "spend": "11714.93"
        }, 
        {
            "clicks": "8785.17", 
            "conversions": "1064.87", 
            "date": "2020-01-06", 
            "impressions": "2706542.27", 
            "spend": "7099.13"
        }, 
        {
            "clicks": "14264.91", 
            "conversions": "1729.08", 
            "date": "2020-01-07", 
            "impressions": "4394744.42", 
            "spend": "11527.2"
        }]
    assert json.loads(response.data) == test_data
```

Now that this works, we know how to test cloud functions locally.

If we wanted to test the Facebook function, we could do this via Mocks, where we mimic the response data you'd expect to get from Facebook. However in this case it's some strange 'cursor' object which I don't know how to convert into a real python object, except by doing the exact data transformation we'd be testing for in our test! 

So essentially in this case test coverage would be kind of useless for us. It would be adding overhead with no real gain, since any bug in my code for the function, would also show up one to one as a bug in the way I implement the test. 

It does make sense to add test cases for this eventually, and learn how to do mocks etc, but if we want to move fast we have to think carefully about whether the increase in relaibility and predictability (likely a small improvement in this case, if at all) would ultimately be worth the research time needed (which could be hours, maybe days, it's hard to know when solving a new challenge).

For now that concludes our tutorial on testing - you have most of the building blocks for building your own tests, and definitely feel free to submit a pull request with the tests you add.

