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
```

Rather than messing with the signup routes and finding a way to fake the form field, instead let's just test the User model directly.



create(name, email, password)

def_test_sign_up(tester):

def sign_up(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)



- ~~Visit the homepage~~
- ~~Sign up and sign out~~
- Log in and edit your profile
- Create a team
- Add account id and conversion event to team
- Connect Facebook ads
- Invite a user to a team
- Log in as invited user
- Visit the generic dashboard
- Visit the Facebook dashboard

