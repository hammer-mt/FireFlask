from flask_login import UserMixin
from app import pyr_auth, pyr_store, pyr_db
from firebase_admin import auth
import os
import tempfile
from hashlib import md5

class User(UserMixin):
    def __init__(self, uid, email, name, verified, created, photo_url):
        self.id = uid
        self.email = email
        self.name = name
        self.verified = verified
        self.created = created
        self.photo_url = photo_url
    
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
                created=firebase_user.user_metadata.creation_timestamp,
                photo_url=firebase_user.photo_url
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
            created=firebase_user.user_metadata.creation_timestamp,
            photo_url=firebase_user.photo_url
        )
        return flask_user

    @staticmethod
    def auth(email, password):
        pyr_user = pyr_auth.sign_in_with_email_and_password(email, password)
        pyr_user_info = pyr_auth.get_account_info(pyr_user['idToken'])

        is_verified = pyr_user_info['users'][0]['emailVerified']

        # if not is_verified:
        #     # send verification
        #     pyr_auth.send_email_verification(pyr_user['idToken'])
        #     print("Sent email verification")

        firebase_user = auth.get_user(pyr_user['localId'])

        print('Sucessfully signed in user: {0}'.format(pyr_user['localId']))
        flask_user = User(
            uid=pyr_user['localId'],
            email=pyr_user['email'],
            name=pyr_user['displayName'],
            verified=is_verified,
            created=pyr_user_info['users'][0]['createdAt'],
            photo_url=firebase_user.photo_url
        )
        return flask_user

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
        meta = pyr_db.child('users').child(self.id).get().val()
        return meta

    def set_meta(self, job_title):
        pyr_db.child('users').child(self.id).set({
            "job_title": job_title
        })

    def upload(self, photo):

        temp = tempfile.NamedTemporaryFile(delete=False)

        # Save temp image
        photo.save(temp.name)

        pyr_store.child('profiles/{}/{}'.format(self.id, temp.name)).put(temp.name)

        photo_url = pyr_store.child('profiles/{}/{}'.format(self.id, temp.name)).get_url(None)

        auth.update_user(
            self.id,
            photo_url=photo_url
        )
        self.photo_url = photo_url

        # Clean-up temp image
        temp.close()
        os.remove(temp.name)

        return photo_url

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @staticmethod
    def get_by_email(email):
        try:
            firebase_user = auth.get_user_by_email(email)

            print('Successfully fetched user data: {0}'.format(firebase_user.uid))
            flask_user = User(
                uid=firebase_user.uid,
                email=firebase_user.email,
                name=firebase_user.display_name,
                verified=firebase_user.email_verified,
                created=firebase_user.user_metadata.creation_timestamp,
                photo_url=firebase_user.photo_url
            )
            return flask_user

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def invite(email):
        temp_pass = md5(email.lower().encode('utf-8')).hexdigest()

        # invite and send password reset
        pyr_user = pyr_auth.create_user_with_email_and_password(email, temp_pass)
        pyr_auth.send_password_reset_email(email)

        pyr_user_info = pyr_auth.get_account_info(pyr_user['idToken'])

        print(pyr_user)
        print(pyr_user_info)

        flask_user = User(
            uid=pyr_user['localId'],
            email=pyr_user['email'],
            name="",
            verified=False,
            created=pyr_user_info['users'][0]['createdAt'],
            photo_url=""
        )
        return flask_user

    def destroy(self):
        auth.delete_user(self.id)
        print(f"Deleted user {self.id}")




    






