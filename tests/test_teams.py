from app.teams.models import Team, Membership
from app.auth.models import User

def test_create_team(team):
    assert team.name == 'Team Tester'

def test_update_team(team):
    team.update('Team Tester 2', '123456789', 'landing_page_view')

    team = Team.get(team.id)

    assert team.name == 'Team Tester 2'
    assert team.account_id == '123456789'
    assert team.conversion_event == 'landing_page_view'

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