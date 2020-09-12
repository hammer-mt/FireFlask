### 13: Creating a testing suite
In the early days of a project you probably just want to get on with building, and maybe you aren't even sure if your idea will work. As time goes on and complexity increases, it can become more difficult to make improvements without accidentally breaking something. This is where a well-implemented test suite can help – it can give you confidence in your code because you can run it after every change, and catch any bugs before you deploy. This is one of the main concepts that separates data scientists and software engineers – the closest we normally get to testing is running a cell in a Jupyter Notebook. When you have a tool in production though, it quickly becomes a good idea to learn!

We'll be piecing together our testing code from various resources across the web.
- [Testing Flask Applications](https://flask.palletsprojects.com/en/1.1.x/testing/)
- [Mocking External APIs in Python](https://realpython.com/testing-third-party-apis-with-mocks/)
- [Testing External APIs With Mock Servers](https://realpython.com/testing-third-party-apis-with-mock-servers/)
- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Unit Testing and Test-Driven Development in Python](https://www.linkedin.com/learning/unit-testing-and-test-driven-development-in-python)
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

These may be primarily integration tests, as they describe multiple components working together at once to generate a user-visible behavior. We will also want to run unit tests for each function in our project, so we know all our individual functions are working.

