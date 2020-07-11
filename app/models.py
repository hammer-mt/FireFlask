from flask_login import UserMixin
from app import pyr_auth
from firebase_admin import auth
from flask_login import login_user, logout_user

class User(UserMixin):
    def __init__(self, uid, email, name):
        self.id = uid
        self.email = email
        self.name = name
    
    @staticmethod
    def get(user_id):
        try:
            firebase_user = auth.get_user(user_id)
            print('Successfully fetched user data: {0}'.format(firebase_user.uid))

            flask_user = User(
                uid=firebase_user.uid,
                email=firebase_user.email,
                name=firebase_user.display_name
            )
            return flask_user
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def create(name, email, password):
        firebase_user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )
        print('Sucessfully created new user: {0}'.format(firebase_user.uid))

        flask_user = User(
            uid=firebase_user.uid,
            email=firebase_user.email,
            name=firebase_user.display_name
        )
        login_user(flask_user, remember=True)
        return flask_user

    @staticmethod
    def auth(email, password):
        pyr_user = pyr_auth.sign_in_with_email_and_password(email, password)
        print('Sucessfully signed in user: {0}'.format(pyr_user['localId']))
        flask_user = User(
            uid=pyr_user['localId'],
            email=pyr_user['email'],
            name=pyr_user['displayName']
        )
        login_user(flask_user, remember=True)
        return flask_user

    @staticmethod
    def logout():
        logout_user()



