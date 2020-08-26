# FireFlask

Fireflask is a boilerplate template for spinning up a Python Flask application with a Firebase NoSQL database / cloud function backend, and Materalize CSS.

This is my attempt to make a kind of [rails for saas](https://www.indiehackers.com/post/ror-saas-boilerplate-app-market-need-fb7af3d8db)' boilerplate template, something that [implements 90% of the same features](https://twitter.com/parkerconrad/status/1297696630355816448?s=03) that [every SaaS application needs](https://twitter.com/2michaeltaylor/status/1275132718729375746?s=20), but on a Python backend with NoSQL so it's an accessible next step to any data scientist graduating from jupyter notebooks and building a B2B SaaS application for marketing. 

## Live example
[[https://fireflask-ef97c.uc.r.appspot.com]([https://fireflask-ef97c.uc.r.appspot.com)

## Built by
- Michael Taylor [https://twitter.com/2michaeltaylor](https://twitter.com/2michaeltaylor)
- Founder of [Saxifrage.xyz](https://www.saxifrage.xyz/)

## How to use

*** Note: I'm assuming you're on Windows and have Gcloud setup ***

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

- You don't need Google Analytics unless you plan to use it.
- Click on web and give the app a nickname, no need for hosting

### Configuration
Get the API key and then create a .flaskenv file in the project folder that looks like this
```
FIREBASE_API_KEY=your-api-key-goes-here
FLASK_APP=main.py
FLASK_DEBUG=1
ACCESS_TOKEN=abc123
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

Download a service account by going to gear icon > project settings > service accounts > generate new private key > generate key

Save it in the app folder and call it
`firebase-private-key.json`

In firebase go to authentication > Signin method > Email/Password and turn it on.

Also go to Storage and click get started, save the default name and it should then be active.

Go to realtime database and click create database. Start in locked mode.

Copy these rules and paste across into the realtime database rules.

```
{
  /* Visit https://firebase.google.com/docs/database/security to learn more about security rules. */
  "rules": {
    ".read": false,
    ".write": false,
    "memberships": {
      ".indexOn": ["team_id", "user_id"]
    }
  }
}
```


### Google Cloud Function
We also need to deploy the cloud function for loading data.

Deactivate our virtual env
`deactivate`

Then create your new virtual env
`python -m venv functions\get_test_data_venv`
`functions\get_test_data_venv\Scripts\activate`

Install the requirements of the cloud function.
`pip install -r functions\get_test_data\requirements.txt`

Add the environment variables like this if in powershell (vscode)
`$env:APP_ID="123456"`
`$env:APP_SECRET="abcdef"`

Or like this if in command line
`set APP_ID=123456`
`set APP_SECRET=abcdef`

To check it's working, run this:
`python functions/get_test_data/main.py`

Visit `http://localhost:5000/?access_token=123456&account_id=123456789&date_start=2020-01-01&date_end=2020-01-07`

`CTRL C` to exit the flask server

Go into Google Firebase and upgrade to Blaze so you can deploy cloud functions. (Spark > Upgrade > Blaze > Purchase)

It shouldn't cost much but I recommend you set a budget alert just in case.

We also need to create a container, so we need to enable this:
`gcloud config set project my-project-1234`
`gcloud services enable cloudbuild.googleapis.com`

Now let's deploy this with the environment variables.

`gcloud beta functions deploy get_test_data --trigger-http --runtime python37 --project my-project-1234 --source .\functions\get_test_data --allow-unauthenticated --entry-point=main --update-env-vars APP_ID=123456,APP_SECRET=abcdef`

If so just click that link and enable cloud build.

Once we run this successfully, we should be able to test it by visiting `https://us-central1-my-project-1234.cloudfunctions.net/get_test_data?access_token=123456&account_id=123456789&date_start=2020-01-01&date_end=2020-01-07`

Now we're done testing the function, we can move on back to integrating it with our dashboard.

`deactivate` to exit the venv


### Facebook Connector
Now if you want to use the Facebook connector you need to create a Facebook app.

First we need to make a new Facebook app by visiting here: [https://developers.facebook.com/apps/](https://developers.facebook.com/apps/)

Click to add new app and choose business integrations.

Give it a name, contact email and select if you're just using it for yourself or for others. You can also choose to connect it to a business manager.

Copy the app ID (should be at the top of the page) and the app secret (in settings > basic). While you're there, add to the App Domains:
`127.0.0.1:5000`
and
`my-project-1234.uc.r.appspot.com`

Add the Facebook login product and change the `Embedded Browser OAuth Login` setting to YES

Add this to the Valid OAuth Redirect URIs
`https://127.0.0.1:5000/connectors/facebook/callback`
`https://fireflask-ef97c.uc.r.appspot.com/connectors/facebook/callback`

`https://127.0.0.1:5000/connectors/facebook/callback`
`https://ladder-115e5.uc.r.appspot.com/connectors/facebook/callback`

Add the following to your config.py class

```
CONNECTORS = {
    "facebook_app_id": "123456789",
    "facebook_app_secret": os.environ.get('FACEBOOK_APP_SECRET'),
    "facebook_authorization_endpoint": "https://www.facebook.com/v6.0/dialog/oauth",
    "facebook_token_endpoint": "https://graph.facebook.com/v6.0/oauth/access_token"
}
```

Then in your flaskenv file add the facebook app secret:
`FACEBOOK_APP_SECRET=abcdefghijklmnopqrstuvwxyz`

We also need to deploy the cloud function for Facebook.

Deactivate our virtual env if you have one running.
`deactivate`

Then create your new virtual env
`python -m venv functions\get_facebook_data_venv`
`functions\get_facebook_data_venv\Scripts\activate`

Install the requirements of the cloud function.
`pip install -r functions\get_facebook_data\requirements.txt`

Add the environment variables like this if in powershell (vscode)
`$env:FACEBOOK_APP_ID="123456"`
`$env:FACEBOOK_APP_SECRET="abcdef"`

Or like this if in command line
`set FACEBOOK_APP_ID=123456`
`set FACEBOOK_APP_SECRET=abcdef`

To check it's working, run this:
`python functions/get_facebook_data/main.py`

Get an access token by visiting here and choosing your app, then clicking generate token
`https://developers.facebook.com/tools/explorer/`

Run this query in the graph explorer to get a list of ad accounts
`me?fields=id,name,adaccounts{name}`

Visit `http://localhost:5000/?access_token=<token>&account_id=<account>&date_start=2020-01-01&date_end=2020-01-20&conversion_event=<event>`

`CTRL C` to exit the flask server

Now let's deploy this with the environment variables.

`gcloud beta functions deploy get_facebook_data --trigger-http --runtime python37 --project my-project-1234 --source .\functions\get_facebook_data --allow-unauthenticated --entry-point=main --update-env-vars FACEBOOK_APP_ID=123456,FACEBOOK_APP_SECRET=abcdef`

Once we run this successfully, we should be able to test it by visiting `https://us-central1-my-project-1234.cloudfunctions.net/get_facebook_data?access_token=<token>&account_id=<account>&date_start=2020-01-01&date_end=2020-01-20&conversion_event=<event>`

Now we're done testing the function, we can move on back to integrating it with our dashboard.

`deactivate` to exit the venv

### Deployment
Great, everything should work. Feel free to delete this readme.md, the todo.md, license, and anything not needed for your project.

To run the project locally, first reactivate your main script
`venv\Scripts\activate` to reactivate your main venv

then run flask like this:
`flask run --cert=adhoc`

Check everything is as you expect, and make any customizations for your use case as necessary.
- Sign up and sign out
- Log in and edit your profile
- Create a team
- Add account id and conversion event to team
- Connect Facebook
- Invite a user to a team
- Log in as invited user
- Visit the dashboard
- Visit the Facebook dashboard

Once you're ready to deploy to production on Google App Engine, follow these steps:

`CTRL + C` to exit the server

Add an env.yaml file
```
env_variables:
    FLASK_APP: main.py
    FIREBASE_API_KEY: abcdefghijklmnopqrstuvwxyz123456789
    ACCESS_TOKEN: abc123
    FACEBOOK_APP_SECRET: abc123
```

Now is a good time to check into github and make sure none of your sensitive passowrds are there.

`git status`

If you do see something in there that shouldn't be, like an env folder or something, remove it like this:
`git rm --cached functions/get_test_data_venv/Scripts/easy_install.exe`

or the whole folder like this:
`git rm -r --cached functions/get_test_data_venv`

Now you can commit:
`git add .`
`git commit -m "committing before deployment"`
`git push`

Now set the default project to work on.

`gcloud config set project my-project-12435`

Now deploy:
`gcloud app deploy`

You can see the app if you type
`gcloud app browse`