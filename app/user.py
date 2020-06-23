from flask_login import UserMixin
from app import db, auth

class User(UserMixin):
    def __init__(self, id_, email, name, token):
        self.id = id_
        self.email = email
        self.name = name
        self.token = token
    
    @staticmethod
    def get(user_id):
        try:
            cred = auth.get_account_info(user_id)
            meta = db.child('users').get(cred.uid).val()
            user = User(
                id_=cred['idToken'],
                email=cred['email'],
                name=meta['name'],
                token=meta['token']
            )
            return user
        except:
            return None

    @staticmethod
    def create(name, email, password):
        try:
            cred = auth.create_user_with_email_and_password(email, password)
            token = auth.create_custom_token(cred.uid)
            db.child('users').child(cred.uid).set({
                "name": name,
                "token": token
            })
            user = User(
                id_=cred['idToken'],
                email=email,
                name=name,
                token=token
            )
            return user
        except:
            return None

    @staticmethod
    def auth(email, password):
        try:
            cred = auth.sign_in_with_email_and_password(email, password)
            meta = db.child('users').get(cred.uid).val()
            auth.refresh(cred['refreshToken'])
            user = User(
                id_=cred['idToken'],
                email=cred['email'],
                name=meta['name'],
                token=meta['token']
            )
            return user
        except:
            return None

    @staticmethod
    def reset(email):
        auth.send_password_reset_email(email)

    def logout(self):
        auth.current_user = None

    def update(self, meta):
        uid = auth.current_user.uid
        db.child("users").child(uid).update(meta)