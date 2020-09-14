import pytest
from app import create_app
from config import Config

print(Config.DB.get('FIREBASE_API_KEY'))


class TestConfig(Config):
    TESTING = True

@pytest.fixture()
def tester():
    app = create_app(TestConfig)

    with app.app_context():
        tester = app.test_client()
        yield tester