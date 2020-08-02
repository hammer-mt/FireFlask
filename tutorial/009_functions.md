### 9: Adding Cloud Functions

The goal of this section is to integrate google cloud functions in a modularized way, so you can have core parts of your app running serverless (and therefore not dependent on where you host). This will let us scale up indefinitely with google cloud functions to do the heavy lifting, meaning our application won't hang when making requests. We will however still make the functions available as part of the application for testing purposes.

- [Serverless Python Quickstart with Google Cloud Functions](https://dev.to/googlecloud/serverless-python-quickstart-with-google-cloud-functions-19bb)

The way cloud functions are structured, is as a main.py file and a requirements.txt file saved in a single folder. Let's keep all our cloud functions in one section outside the app in the main fireflask folder. Our first function will just simulate pulling cost, clicks, impressions, conversions, data from an ad platform, broken down by day. We'll add actual connections to Facebook and Google into the project in the future.

Let's create a folder within the new functions directory that's called 'get_test_data'. It needs a main.py file and a requirements.txt file (blank for now). In the main.py file let's just add a function that returns hello world.

```
def hello(request):
    return "Hello World!"
```

Now we need to add the ability to run the function locally. To do this add the code below.

```
if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)
    app.route('/')(lambda: hello(request))
    app.run()
```

Next exit the virtual environment you made for your core flask app:
`deactivate`

Then create a new virtual environment just for this function, in the functions folder.
```
cd functions
python -m venv get_test_data_venv
.\get_test_data_venv\Scripts\activate
```

Now you're in your virtual environment just for that cloud function, install flask there.
`pip install flask`

Google Cloud will already have flask installed as default, but anyway it'll be useful to see how we save requirements for a cloud function. To do so we use the same 'pip freeze' command but instead save it to the requirements in the cloud function folder.

`pip freeze > get_test_data/requirements.txt`

Now let's run the function locally and check it worked.
`python main.py`

You should see 'hello world'. Now let's add in the ability to pass parameters.

```
def hello(request):
    name = request.args.get('name', 'World')
    return f"Hello {name}!"
```

Restart the server, and then when you visit `http://localhost:5000/?name=Mike` you should see 'Hello Mike'.

Now exit the server `ctrl + c` and `deavtivate` the virtual env.

Let's set ourselves up to be able to deploy on Google Cloud.

Go to this page and follow the instructions (make sure you tick 'beta commands' to install that component):
https://cloud.google.com/sdk/docs/

This should open up your main terminal (I can't figure out how to get it in VS Code).

To deploy the cloud function you do this line:

`gcloud beta functions deploy get_test_data --trigger-http --runtime python37 --project fireflask-ef97c --source C:\Users\Hammer\Documents\Projects\FireFlask\functions\get_test_data --allow-unauthenticated --entry-point=hello`

To explain this:
- get_test_data is what we're calling the function
- trigger-http makes it a http API (rather than say a cron job)
- python 3.7 runtime
- specify your project name
- specify where that project lives (you can also just cd into the directory and leave this part)
- allow unauthenticated uses which lets you call the API without logging in
- entry point is which function to run when the API is called

More info on cloud functions here:
`https://cloud.google.com/sdk/gcloud/reference/functions/deploy`

Now we can go to `https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data?name=Mike` and get the same response we got last time. But this time it's live on the web!

We'll cover testing authenticated cloud functions in a later section.

For our final function we will want to follow the pattern the major ad platforms follow:

1/ You pass in app_id, app_secret and access_token (for the user)
2/ You get back data broken down by time increment (daily for our case)
3/ Then we do something with the data to visualize it

[Guide to Facebook Insights API (Part 2)](https://www.damiengonot.com/blog/guide-facebook-insights-api-2)

The data format we expect is this:
```
[{
    "date": "2020-01-09",
    "spend": "8000.00",
    "clicks": "9900",
    "impressions": "3050000",
    "conversions": "1200"
}, {
    "date": "2020-01-10",
    "spend": "8200.00",
    "clicks": "10000",
    "impressions": "3500000",
    "conversions": "1300"
}, {
    "date": "2020-01-11",
    "spend": "10000.00",
    "clicks": "10900",
    "impressions": "3200000",
    "conversions": "1400"
}, {
    "date": "2020-01-12",
    "spend": "9000.00",
    "clicks": "12000",
    "impressions": "3700000",
    "conversions": "1000"
}, {
    "date": "2020-01-13",
    "spend": "7000.00",
    "clicks": "8000",
    "impressions": "3000000",
    "conversions": "800"
}, {
    "date": "2020-01-14",
    "spend": "8000.00",
    "clicks": "9000",
    "impressions": "3200000",
    "conversions": "1000"
}, {
    "date": "2020-01-15",
    "spend": "11000.00",
    "clicks": "12000",
    "impressions": "4000000",
    "conversions": "1500"
}]
```

So let's put this in the response for our cloud function. We also need to grab the access_token from the request.

`access_token = request.args.get('access_token')`

Now we'll need to pass an access token instead of our 'name' parameter.

We also want to pull the environment variables for the app id and app secret. To do this we need to pass environment variables to our cloud function when we deploy, like this:

`--update-env-vars FOO=bar,BAZ=boo`

But to test locally, we need to export to the environment. So first activate our venv again:

`.\get_test_data_venv\Scripts\activate`

Then set the environment variables like this:

`$env:APP_ID="123456"`
`$env:APP_SECRET="abcdef"`

Now set the file to pull from the os.environ to get the secret and id.

```
app_id = os.environ.get('APP_ID')
app_secret = os.environ.get('APP_SECRET')
```

Finally you want to just check they're all present before sending the data (we could look them up against a list of allowed values, but for now just checking they're there is good enough).

```
if app_id and app_secret and access_token:
        return jsonify(data)
    else:
        return None
```

Note we JSONIFY the data so it's in the right format (flask can't return a list).

Now run the flask app again:
`python get_test_data/main.py`

If we visit `http://localhost:5000/?access_token=Mike`

We should see a JSON response with the data.

Now let's deploy this with the environment variables. Note we changed the function name to main now so we need to update the entry point also.

`gcloud beta functions deploy get_test_data --trigger-http --runtime python37 --project fireflask-ef97c --source C:\Users\Hammer\Documents\Projects\FireFlask\functions\get_test_data --allow-unauthenticated --entry-point=main --update-env-vars APP_ID=123456,APP_SECRET=abcdef`

Once we run this, we should be able to test it by visiting `https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data?access_token=Mike`

At this point remember to save to git as usual.
`git checkout -b "functions"`
`git add .`
`git commit -m "deployed cloud function" `
`git push --set-upstream origin functions`

Next up we need to call this function within one of our routes, then display it on the page. Let's do it on the index page after logging in, for simplicity.

Deactivate the environment and get back to the main branch.
`deactivate`
`cd ..`

Then go into the main folder in the app, and add this to the imports
`from flask_login import current_user`
`import json`
`import requests`

Then in routes for index add this.
```
if current_user.is_authenticated:
        
    # Run the cloud function
    url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data"
    payload = {"access_token": "Mike"}
    response = requests.get(url, params=payload)
    data_json = json.loads(response.text)

    return render_template('main/index.html', title='Home', data=data_json)
```

Add this to the template for index.

```
<!-- Authenticated users -->
{% if current_user.is_authenticated %}
        
<h1>Hi, {{ current_user.name }}!</h1>

{% if data %}

<p>{{ data }}</p>

{% endif %}
```

Activate the venv and run
`venv\Scripts\activate`
`flask run`

Sign in and you should see the data there live on the page.

Let's make the data look nicer by formatting it in a table.

Change the index to 
```
<!-- Cloud function data -->
    {% if data %}
    <div class="row">
        <div class="col s12 m8">
            <div class="card-panel">
                <table class="striped">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Spend</th>
                            <th>Clicks</th>
                            <th>Impressions</th>
                            <th>Conversions</th>
                        </tr>
                    </thead>
                    <tbody>

                    {% for row in data %}

                        <tr>
                            <td>{{ row['date'] }}</td>
                            <td>{{ "${:,.2f}".format(row['spend']|float) }}</td>
                            <td>{{ "{:,}".format(row['impressions']|int) }}</td>
                            <td>{{ "{:,}".format(row['clicks']|int) }}</td>
                            <td>{{ "{:,}".format(row['conversions']|int) }}</td>
                        </tr>

                    {% endfor %}

                    </tbody>
                </table>

    {% endif %}
```
This will format everything nicely in a table.

Note this is using a hardcoded access token - in a future section we'll show how to get an access token per user. If we did want to abstract away the access token for now, we should do this.

Add this to the route:
`from config import Config`

and in the route for index, change it to this:
`payload = {"access_token": Config.ACCESS_TOKEN}`

Add this into the config.py file.
`ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')`

Then the .flaskenv file:
`ACCESS_TOKEN=abc123`

You should never store anything in github that is a password or other type of secret.

Obviously this cloud function doesn't do much - the idea was to show you how to use a cloud function to pull data. You could update the cloud function to pull from an actual API platform, which we'll cover later.

Now save your updates to git and merge branch.
`git add .`
`git commit -m "displayed cloud function data"`
`git push`
`git checkout master`
`git merge functions`
`git push`














