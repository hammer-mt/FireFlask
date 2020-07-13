from flask_login import UserMixin
from app import pyr_auth, db
from firebase_admin import auth
from flask_login import login_user, logout_user

class User(UserMixin):
    def __init__(self, uid, email, name, verified, created):
        self.id = uid
        self.email = email
        self.name = name
        self.verified = verified
        self.created = created
    
    @staticmethod
    def get(user_id):
        try:
            firebase_user = auth.get_user(user_id)
            print('Successfully fetched user data: {0}'.format(firebase_user.uid))
            flask_user = User(
                uid=firebase_user.uid,
                email=firebase_user.email,
                name=firebase_user.display_name,
                verified=firebase_user.email_verified,
                created=firebase_user.user_metadata.creation_timestamp
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

        # send verification
        pyr_user = pyr_auth.sign_in_with_email_and_password(email, password)
        pyr_auth.send_email_verification(pyr_user['idToken'])

        print("Sent email verification")

        flask_user = User(
            uid=firebase_user.uid,
            email=firebase_user.email,
            name=firebase_user.display_name,
            verified=firebase_user.email_verified,
            created=firebase_user.user_metadata.creation_timestamp
        )
        login_user(flask_user, remember=True)
        return flask_user

    @staticmethod
    def auth(email, password):
        pyr_user = pyr_auth.sign_in_with_email_and_password(email, password)
        pyr_user_info = pyr_auth.get_account_info(pyr_user['idToken'])

        is_verified = pyr_user_info['users'][0]['emailVerified']

        if not is_verified:
            # send verification
            pyr_auth.send_email_verification(pyr_user['idToken'])
            print("Sent email verification")

        print('Sucessfully signed in user: {0}'.format(pyr_user['localId']))
        flask_user = User(
            uid=pyr_user['localId'],
            email=pyr_user['email'],
            name=pyr_user['displayName'],
            verified=is_verified,
            created=pyr_user_info['users'][0]['createdAt']
        )
        login_user(flask_user, remember=True)
        return flask_user

    @staticmethod
    def logout():
        logout_user()

    @staticmethod
    def reset(email):
        pyr_auth.send_password_reset_email(email)

    def edit(self, name, email, job_title):
        #email change
        if self.email != email:
            auth.update_user(
                self.id,
                email=email,
                display_name=name,
                email_verified=False,
            )
            self.verified = False
            self.email = email
        
        #just a name or meta change
        else:
            auth.update_user(
                self.id,
                display_name=name,
            )
        
        self.name = name
        self.set_meta(job_title)

    def get_meta(self):
        meta = db.child('users').child(self.id).get().val()
        return meta

    def set_meta(self, job_title):
        db.child('users').child(self.id).set({
            "job_title": job_title
        })


            




        





