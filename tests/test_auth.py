from app.auth.models import User

def test_sign_up(user):
    assert user.email == 'test@example.com'

def test_sign_in(user, password):
    user = User.auth('test@example.com', password)
    assert user.email == 'test@example.com'

def test_edit_profile(user):
    user.edit('tester 2', 'test_2@example.com', 'QA Tester')

    user = User.get(user.id)
    meta = user.get_meta()

    assert user.name == 'tester 2'
    assert user.email == 'test_2@example.com'
    assert meta.get('job_title') == 'QA Tester'