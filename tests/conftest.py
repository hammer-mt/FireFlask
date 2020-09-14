import pytest
from app import create_app
from config import Config
import string
import random
from app.auth.models import User
from app.teams.models import Team, Membership


class TestConfig(Config):
    TESTING = True

@pytest.fixture()
def tester():
    app = create_app(TestConfig)

    with app.app_context():
        tester = app.test_client()
        yield tester

@pytest.fixture()
def password():
    password = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(7))
    yield password

@pytest.fixture()
def user(password):
    name = 'tester'
    email = 'test@example.com'
    user = User.create(name, email, password)

    yield user

    print('')
    user.destroy()

@pytest.fixture()
def team():
    name = 'Team Tester'
    team = Team.create(name)

    yield team
    
    print('')
    team.remove()

    