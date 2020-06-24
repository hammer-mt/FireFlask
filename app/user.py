from flask_login import UserMixin
from app import db, auth

class User(UserMixin):
    def __init__(self, firebase_id, access_token, login_token, refresh_token, email, name):
        self.firebase_id = firebase_id
        self.access_token = access_token
        self.login_token = login_token
        self.refresh_token = refresh_token
        self.email = email
        self.name = name

    def get_id(self):
        return self.firebase_id
    
    @staticmethod
    def get(user_id):
        meta = db.child('users').get(user_id).val()
        cred = auth.get_account_info(meta['access_token'])
        user = User(
            firebase_id=cred['localId'],
            access_token=cred['idToken'],
            refresh_token=cred['refreshToken'],
            email=cred['email'],
            name=meta['name'],
            login_token=meta['login_token']
        )
        return user

    @staticmethod
    def create(name, email, password):
        cred = auth.create_user_with_email_and_password(email, password)
        login_token = auth.create_custom_token(cred['localId'])
        db.child('users').child(cred['localId']).set({
            "name": name,
            "login_token": login_token,
            "access_token": cred['idToken']
        })
        user = User(
            firebase_id=cred['localId'],
            access_token=cred['idToken'],
            refresh_token=cred['refreshToken'],
            email=email,
            name=name,
            login_token=login_token
        )
        return user

    @staticmethod
    def auth(email, password):
        cred = auth.sign_in_with_email_and_password(email, password)
        meta = db.child('users').get(cred['localId']).val()
        user = User(
            firebase_id=cred['localId'],
            access_token=cred['idToken'],
            refresh_token=cred['refreshToken'],
            email=cred['email'],
            name=meta['name'],
            login_token=meta['login_token']
        )
        return user

    @staticmethod
    def reset(email):
        auth.send_password_reset_email(email)

    def logout(self):
        auth.current_user = None

    def update(self, meta):
        uid = auth.current_user.uid
        db.child("users").child(uid).update(meta)
