### 10: Deploying on Cloud Run

Now let's get our application deployed finally so people can visit it on the internet. To do this we'll try cloud run, which is the simplest option for Google Cloud.

- [Deploying a Flask app to Google App Engine](https://medium.com/@dmahugh_70618/deploying-a-flask-app-to-google-app-engine-faa883b5ffab)
- [Deploying Machine Learning has never been so easy](https://towardsdatascience.com/https-towardsdatascience-com-deploying-machine-learning-has-never-been-so-easy-bbdb500a39a)

First let's create our new branch.
`git checkout -b deploy`

Now add your updates
`git add .`
`git commit -m "added updates"`

Commit them by setting upstream
`git push --set-upstream origin deploy`

We need to install gunicorn to run the server on production (flask run isn't suitable).
`pip install gunicorn`
`pip freeze > requirements.txt`

Now let's make an app.yaml file which is needed by google app engine.

```

runtime: python37
entrypoint: gunicorn -b :$PORT --timeout 100 main:app

includes:
    - env.yaml
```

We keep our environment variables hidden in a different file env.yaml, that we don't upload to source code.
```
env_variables:
    FLASK_APP: main.py
    FIREBASE_API_KEY: abcdefghijklmnopqrstuvwxyz123456789
    ACCESS_TOKEN: abc123
```

Make sure to add that to the .gitignore
`env.yaml`

We already have gcloud installed from deploying the cloud functions. So go to your main terminal and install app engine for python.

`gcloud components install app-engine-python`

This will pop out a new terminal, make sure to hit y, then hit enter when it pauses after creating an update staging area.

Now set the default project to work on.

`gcloud config set project fireflask-ef97c`

We need to set up billing, by upgrading our plan in firebase. If you upgrade from spark plan, you can then run the next command successfully.

We also need to create a container, so we need to enable this:

`gcloud services enable cloudbuild.googleapis.com`

Now we're ready to deploy, we just need to get to the right folder:

`cd C:\Users\Hammer\Documents\Projects\FireFlask\`

Now deploy:
`gcloud app deploy`

You can see the app if you type
`gcloud app browse`

However we have an issue - we are deploying tonnes of files:
` gcloud meta list-files-for-upload`

So we need to create a .gcloudignore file, similar to .gitignore.

Make sure you get rid of virtual envs.
```
venv/
*venv/
```

Make sure you add the _venv from your cloud functions to your .gitignore too.
`*venv/`

Also makes sense to add any readme or text files not needed in deploy.
```
# Get rid of text files
tutorial/
todo.md
readme.md
LICENSE
```

You can check it with 
`gcloud meta list-files-for-upload`

Should just see the main files now, not thousands.

The steps to deploy again should be:

`cd C:\Users\Hammer\Documents\Projects\FireFlask\` <!-- only if you changed directories -->
`gcloud config set project fireflask-ef97c` <!-- only if you changed projects -->
`gcloud app deploy`
`gcloud app browse`

