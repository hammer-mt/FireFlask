import string
import random
from app.auth.models import User
from flask_login import current_user, login_user


def test_sign_up(tester):
    name = 'tester'
    email = 'test@example.com'
    password = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(7))
    print(name, email, password)
    user = User.create(name, email, password)
    login_user(user)
    assert current_user.email == email
    user.destroy()