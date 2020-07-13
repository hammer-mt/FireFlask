# FireFlask

Fireflask is a boilerplate template for spinning up a Python Flask application with a Firebase NoSQL database / cloud function backend, and Materalize CSS.

This is my attempt to make a kind of [rails for saas](https://www.indiehackers.com/post/ror-saas-boilerplate-app-market-need-fb7af3d8db)' boilerplate template, something that implements 90% of the same features [every SaaS application needs](https://twitter.com/2michaeltaylor/status/1275132718729375746?s=20), but on a Python backend with NoSQL so it's an accessible next step to any data scientist graduating from jupyter notebooks. 

## How to use

Navigate to your project folder and run this command (replace MyProjectName)
`git clone git@github.com:mjt145/FireFlask.git MyProjectName`

Move into that folder you created.
`cd MyProjectName`

Open with your code editor
`code .`

Create a virtual environment with this command.
`python -m venv venv`

Activate it with this command on windows.
`venv\Scripts\activate`

Install the requirements.
`pip install -r requirements.txt`

Remove the old github repository.
`git remote rm origin`

Create a new repository and get the URL or SHH, then use in this command.
`git remote add origin git@github.com:mjt145/MyProjectName.git`

Now git push while setting the upstream
`git push --set-upstream origin master`

You now need to go to Firebase and make a new project.

Get the API key and then create a .flaskenv file that looks like this
```
FIREBASE_API_KEY=your-api-key-goes-here
FLASK_APP=fireflask.py
FLASK_DEBUG=1
```

Update the values in the config.py
```
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)

    DB = {
        "apiKey": os.environ.get('FIREBASE_API_KEY'),
        "authDomain": "my-project-1234.firebaseapp.com",
        "databaseURL": "https://beck-7e412.firebaseio.com",
        "projectId": "my-project-1234",
        "storageBucket": "my-project-1234.appspot.com",
        "messagingSenderId": "123456789",
        "appId": "1:123456789:web:1a2b3c4d5e6f7g8h9i",
        "serviceAccount": "app/firebase-private-key.json"
    }
```

Download a service account by going to project settings > service accounts > generate new private key > generate key

 in the app folder and call it
`firebase-private-key.json`

Finally in firebase go to authentication > Signin method > Email/Password and turn it on.

Great, everything should work. Feel free to delete this readme.md, the todo.md, license, and anything not needed for your project.

To run the project use 
`flask run`