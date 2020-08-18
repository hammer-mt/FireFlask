from app import pyr_auth, pyr_db
from firebase_admin import auth

            
class Team():
    def __init__(self, id_, name, account_id, facebook_token=None):
        self.id = id_
        self.name = name
        self.account_id = account_id
        self.facebook_token = facebook_token
    
    @staticmethod
    def get(team_id):
        team_data = pyr_db.child('teams').child(team_id).get().val()
        team = Team(
            id_=team_id, 
            name=team_data['name'],
            account_id=team_data.get('account_id'),
            facebook_token=team_data.get('facebook_token')
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

    def update(self, name, account_id):
        pyr_db.child('teams').child(self.id).update({
            "name": name,
            "account_id":account_id 
        })

        self.name = name
        self.account_id = account_id

    def facebook_connect(self, token):
        pyr_db.child('teams').child(self.id).update({
            "facebook_token": token,
        })

        self.facebook_token = token




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

    def update(self, role):
        pyr_db.child('memberships').child(self.id).update({
            "role": role
        })

        self.role = role

    @staticmethod
    def get_users_by_team(team_id):
        users_by_team = pyr_db.child("memberships").order_by_child("team_id").equal_to(team_id).get()

        return users_by_team

    @staticmethod
    def get_teams_by_user(user_id):
        teams_by_user = pyr_db.child("memberships").order_by_child("user_id").equal_to(user_id).get()

        return teams_by_user

    @staticmethod
    def user_role(user_id, team_id):
        users_by_team = pyr_db.child("memberships").order_by_child("team_id").equal_to(team_id).get()

        role = None
        for membership in users_by_team:
            membership_data = membership.val()

            if membership_data['user_id'] == user_id:
                role = membership_data['role']
        
        return role

    def remove(self):
        pyr_db.child('memberships').child(self.id).remove()




    






