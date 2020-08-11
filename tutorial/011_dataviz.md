### 11: Visualizing Data

Next up we'll be visualizing our data with chart.js. 

- [https://www.patricksoftwareblog.com/creating-charts-with-chart-js-in-a-flask-application/](https://www.patricksoftwareblog.com/creating-charts-with-chart-js-in-a-flask-application/)
- [https://blog.ruanbekker.com/blog/2017/12/14/graphing-pretty-charts-with-python-flask-and-chartjs/](https://blog.ruanbekker.com/blog/2017/12/14/graphing-pretty-charts-with-python-flask-and-chartjs/)
- [https://towardsdatascience.com/flask-and-chart-js-tutorial-i-d33e05fba845](https://towardsdatascience.com/flask-and-chart-js-tutorial-i-d33e05fba845)
- [https://medium.com/@crawftv/javascript-jinja-flask-b0ebfdb406b3](https://medium.com/@crawftv/javascript-jinja-flask-b0ebfdb406b3)
- [https://medium.com/@data.corgi9/real-time-graph-using-flask-75f6696deb55](https://medium.com/@data.corgi9/real-time-graph-using-flask-75f6696deb55)
- [https://tobiasahlin.com/blog/chartjs-charts-to-get-you-started/](https://tobiasahlin.com/blog/chartjs-charts-to-get-you-started/)

First let's create our new branch.
`git checkout -b dataviz`

Now add your updates
`git add .`
`git commit -m "added updates"`

Commit them by setting upstream
`git push --set-upstream origin dataviz`

Add the chart.js visualizations on 
`<link href="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.css" rel="stylesheet">`
`<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>`

Note we used the bundled build, which includes moment.js for ChartJS to use for time series graphs.

First let's play around with the index view to add charts there and prove our use case.

We need to get the data in the right format to display. This happens in the routes.py file.

Modify it to contain this:
```

labels = [row['date'] for row in data_json]
values = [row['spend'] for row in data_json]

return render_template('main/index.html', title='Home', data=data_json, labels=labels, values=values)
```

Then use the data to display the chart in the index template.

```
<!-- Chart JS Bar Chart -->
<div class="row">
    <div class="col s12 m6 l6">
        <div class="card-panel">
            <canvas id="barChart" width="200" height="100"></canvas>
        </div>
    </div>

<script>
var ctx = document.getElementById('barChart').getContext('2d');
var barChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [{% for item in labels %}
                    "{{item}}",
                {% endfor %}],
        datasets: [{
            label: 'Spend',
            data:   [{% for item in values %}
                        "{{item}}",
                    {% endfor %}],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
</script>
```

You can also add a line chart like this:
```
<!-- Chart JS line chart -->
   
    <div class="col s12 m6 l6">
        <div class="card-panel">
            <canvas id="lineChart" width="200" height="100"></canvas>
        </div>
    </div>
</div>

<script>
var ctx = document.getElementById('lineChart').getContext('2d');
var lineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [{% for item in labels %}
                    "{{item}}",
                {% endfor %}],
        datasets: [{
            label: 'Spend',
            data:   [{% for item in values %}
                        "{{item}}",
                    {% endfor %}],
            fill: true,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            spanGaps: false
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
</script>

```

Note that pylint might give you a lot of errors here, don't worry you can ignore them for now.

It can help to show the chart cards a bit closer to the table, so add this to the main.css.
```
.row {
    margin-bottom: 0em;
}
```

Let's save our progress now.

`git status`
`git add .`
`git commit -m "demonstrated chart`
`git push`

Now we want to refactor this so each chart is called seperately. So let's move this logic over to a separate 'charts' blueprint.

Create a folder in app called 'charts' and add an __init__.py file that has these contents.
```
from flask import Blueprint

bp = Blueprint('charts', __name__)

from app.charts import routes
```

Also add a routes.py file and a folder in templates called charts as well.

We should also add this to the app's init file.
```
from app.charts import bp as charts_bp
app.register_blueprint(charts_bp, url_prefix='/charts')
```

Now let's take the logic out of index. Replace the code in the index.html template with this
```
<div class="row">
    <div class="col s6 m3">
        <a href="{{ url_for('charts.dashboard') }}">
            <div class="card-panel">
                Go to dashboard
            </div>
        </a>    
    </div>
</div>
```

Then create a file called 'dashboard.html' in templates/charts that looks like this:
```
{% extends "main/base.html" %}

{% block content %}

    <h2>Dashboard</h2>

    <!-- Chart JS Bar Chart -->
    <div class="row">
        <div class="col s12 m6 l6">
            <div class="card-panel">
                <canvas id="barChart" width="200" height="100"></canvas>
            </div>
        </div>

    <!-- Chart JS line chart -->
   
        <div class="col s12 m6 l6">
            <div class="card-panel">
                <canvas id="lineChart" width="200" height="100"></canvas>
            </div>
        </div>
    </div>

    <script>
    var data = [{% for item in values %}
                    "{{item}}",
                {% endfor %}];
    var labels = [{% for item in text %}
                    "{{item}}",
                {% endfor %}];


    var ctx = document.getElementById('lineChart').getContext('2d');
    var lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Spend',
                data: data,
                fill: true,
                lineTension: 0.1,
                backgroundColor: "rgba(75,192,192,0.4)",
                borderColor: "rgba(75,192,192,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                spanGaps: false
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    
    var ctx2 = document.getElementById('barChart').getContext('2d');
    var barChart = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Spend',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    </script>

    <!-- Cloud function data -->
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
            </div>
        </div>
    </div>

{% endblock %}
```

Note that we refactored this a little so it declares the data and labels in a javascript variable before loading.

We also changed the name of the labels part we send to the page to text, so let's make sure we change that in our routes as well.

We can strip out the whole cloud function logic from index and move it to the new routes.

```
from flask import render_template
from app.charts import bp
import json
import requests
from config import Config

@bp.route('/', methods=['GET'])
def dashboard():
    # Run the cloud function
    url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data"
    payload = {"access_token": Config.ACCESS_TOKEN}
    response = requests.get(url, params=payload)
    data_json = json.loads(response.text)

    text = [row['date'] for row in data_json]
    values = [row['spend'] for row in data_json]

    return render_template('charts/dashboard.html', title='Dashboard', data=data_json, text=text, values=values)
```

Note we aren't adding login_required yet, so it's easier to test.

Now lets test it out.
`flask run`

That's all working, so now we need to add more types of visualization. 

To make it a little easier to maintain, let's abstract the charts into sub templates.

First we need to abstract away each chart into its own sub template like this:

```
<div class="card-panel">
    <canvas id="barChart" width="200" height="100"></canvas>
</div>

<script>
    var data = [{% for item in values %}
                    "{{item}}",
                {% endfor %}];
    var labels = [{% for item in text %}
                    "{{item}}",
                {% endfor %}];
    
    var ctx = document.getElementById('barChart').getContext('2d');
    var barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Spend',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
</script>
```

That was the bar chart, which we'll put in a file called _bar.html. Do the same for the line chart in _line.html

```
<div class="card-panel">
    <canvas id="lineChart" width="200" height="100"></canvas>
</div>

<script>
    var data = [{% for item in values %}
                    "{{item}}",
                {% endfor %}];
    var labels = [{% for item in text %}
                    "{{item}}",
                {% endfor %}];
    
    
    var ctx = document.getElementById('lineChart').getContext('2d');
    var lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Spend',
                data: data,
                fill: true,
                lineTension: 0.1,
                backgroundColor: "rgba(75,192,192,0.4)",
                borderColor: "rgba(75,192,192,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                spanGaps: false
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    
</script>
```

Then we can also do the same for the table as well.

```
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
</div>
```

Finally let's clean up the charts template by using includes.
```
{% extends "main/base.html" %}

{% block content %}

<h2>Dashboard</h2>

<div class="row">
    <!-- Chart JS Bar Chart -->
    <div class="col s12 m6 l6">
        {% include 'charts/_bar.html' %}
    </div>

    <!-- Chart JS line chart -->
    <div class="col s12 m6 l6">
        {% include 'charts/_line.html' %}
    </div>
</div>

<!-- Data in table -->
<div class="row">
    <div class="col s12 m8">
        {% include 'charts/_table.html' %}
    </div>
</div>

{% endblock %}
```

Now let's refactor the javascript that stores the data, so we won't get a tonne of errors in our templates.

First let's simplify the data we pass.

```
data = json.loads(response.text)

return render_template('charts/dashboard.html', title='Dashboard', data=data)
```

Now we need to process the data in javascript, which goes like this:

```
var chartData = chartData || JSON.parse('{{ data|tojson }}');
var data = [];
var labels = [];
for (i=0; i<chartData.length; i++) {
    data.push(chartData[i]['spend']);
    labels.push(chartData[i]['date']);
}
```

Put that at the top of _bar.html and _line.html. It declares the chartData variable if it doesn't already exist, then processes it in the right format for the chart.

Note the JSON.parse isn't strictly needed (the data object is already JSON) but it removes the errors in your IDE, which for me is an absolute win! If you don't get errors or don't care, use 
`var chartData = chartData || {{ data|tojson }};`

Now let's add a card element, and a donut chart for good measure.

The code for the donut chart looks like this:

```

<div class="card-panel">
    <canvas id="donutChart" width="200" height="317"></canvas>
</div>

{% block javascript %}
<script>
    var chartData = chartData || JSON.parse('{{ data|tojson }}');
    var data = [];
    var labels = [];
    for (i=0; i<chartData.length; i++) {
        data.push(chartData[i]['spend']);
        labels.push(chartData[i]['date']);
    }

    var ctx = document.getElementById('donutChart').getContext('2d');
    var donutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [
            {
              label: "Spend",
              backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850", "#efefefe"],
              data: data
            }
          ]
        },
        options: {
          title: {
            display: true,
            text: 'Spend by day'
          }
        }
    });
    
</script>
{% endblock %}
```

And you want to place it next to the table.
```
<!-- Data in table -->
<div class="row">
    <div class="col s12 m8">
        {% include 'charts/_table.html' %}
    </div>
    <div class="col s6 m4">
        {% include 'charts/_donut.html' %}
    </div>
</div>
```

The metric scorecards should go in a new row at the top.

```
<div class="row">
    <!-- Metric Score Card -->
    <div class="col s4">
        {% include 'charts/_card.html' %}
    </div>

    <!-- Metric Score Card -->
    <div class="col s4">
        {% include 'charts/_card.html' %}
    </div>

    <!-- Metric Score Card -->
    <div class="col s4">
        {% include 'charts/_card.html' %}
    </div>
</div>
```

Then the card itself looks like this:

```
<div class="card">
    <div class="card-content">
        <p>SPEND</p>
        <span class="card-title grey-text text-darken-4">
            {{ "${:,.0f}".format(spend) }}
        </span>
    </div>
</div>
```

We should add this data in the controller, in routes.

```
spend = sum([float(row['spend']) for row in data])

return render_template('charts/dashboard.html', title='Dashboard', data=data, spend=spend)
```

Of course we could keep adding charts, but we have the basics figured out and can see how we would add new visualizations as needed.

Remember to make this dashboard login required now we're done testing.

```
from flask import render_template
from flask_login import login_required
from app.charts import bp
import json
import requests
from config import Config

@bp.route('/', methods=['GET'])
@login_required
def dashboard():
    # Run the cloud function
    url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data"
    payload = {"access_token": Config.ACCESS_TOKEN}
    response = requests.get(url, params=payload)
    data = json.loads(response.text)

    spend = sum([float(row['spend']) for row in data])

    return render_template('charts/dashboard.html', title='Dashboard', data=data, spend=spend)
```

Our users will expect to see the ability to choose date range and client / team, so we need to make it more dynamic. This will mean changes to our cloud function to support this.

Let's adapt our cloud function to accept a date range and account id.

First let's grab the account id and date range from the request.

```
account_id = request.args.get('account_id')
date_start = request.args.get('date_start')
date_end = request.args.get('date_end')
```

Let's process the date range to get the start and end dates.

```
s_date = datetime.strptime(date_start, '%Y-%m-%d')
e_date = datetime.strptime(date_end, '%Y-%m-%d')
delta = e_date - s_date
```

Rather than hardcoding the data, let's use some random number generation to make it look realistic.

However we want the data to be the same pattern each time for debugging, so let's create a random seed from the date range and the account id.

```
epoch = datetime(1970,1,1)
s_since_epoch = (s_date - epoch).days
e_since_epoch = (e_date - epoch).days
random.seed(s_since_epoch + e_since_epoch + int(account_id))
```
Now we can generate some numbers that will always be the same if we chose the same date range and account id.

The random amount we'll shift the numbers by is going to be added to 50%, so we have a range of 0.5 to 1.5.

`shift = random.random() + 0.5`

Final part of adjusting the cloud function is to adapt the data generation to account for the new dynamically generated numbers.

```
data = []
for d in range(delta.days + 1):
    date = datetime.strftime(s_date + timedelta(days=d), '%Y-%m-%d')
    data.append({
        "date": str(date),
        "spend": str(round(8000.00*shift,2)),
        "clicks": str(round(9900*shift, 2)),
        "impressions": str(round(3050000*shift,2)),
        "conversions": str(round(1200*shift,2))
    })
```

Let's test this locally and make sure it works.

`deactivate`
`cd functions`
`.\get_test_data_venv\Scripts\activate`
`$env:APP_ID="123456"`
`$env:APP_SECRET="abcdef"`
`python get_test_data/main.py`

then visit a URL with the right params, like
`http://localhost:5000/?access_token=Mike&account_id=123456789&date_start=2020-01-01&date_end=2020-01-07`

If that's all working, then we're good to deploy.

`gcloud beta functions deploy get_test_data --trigger-http --runtime python37 --project fireflask-ef97c --source C:\Users\Hammer\Documents\Projects\FireFlask\functions\get_test_data --allow-unauthenticated --entry-point=main --update-env-vars APP_ID=123456,APP_SECRET=abcdef`

Then if that works we can visit `https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data?access_token=Mike&account_id=123456789&date_start=2020-01-01&date_end=2020-01-07`

We can also update the route to make sure that works.

```
url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data"
payload = {
    "access_token": Config.ACCESS_TOKEN,
    "account_id": "123456789",
    "date_start": "2020-01-01",
    "date_end": "2020-01-07"
    }
response = requests.get(url, params=payload)
data = json.loads(response.text)
```

now go back and activate your main venv
`deactivate`
`cd ..`
`venv\Scripts\activate`
`flask run`

There we go, dashboard is still working.

Last thing we need to do is accept the date range and account id from the user.

Date range should be pulled from a date picker on the dashboard, and account id should be baked into your team selection. The dashboard should only show once you select a team on the homepage or teams page.

Then the team should show as selected in the navbar, and the account id will be pulled from that team's database.

Lets start with the date picker first.
https://stackoverflow.com/questions/26057710/datepickerwidget-with-flask-flask-admin-and-wtforms
https://materializecss.com/pickers.html

We need to add a new file forms.py in charts
```
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import DateField

class DateForm(FlaskForm):
    start_date = DateField('Start Date', format='%b %d, %Y')
    end_date = DateField('End Date', format='%b %d, %Y')
    submit = SubmitField('RUN QUERY')
```

This gives us the form itself, which we need to load via the routes, which should now look like this.

```
from flask import render_template, request
from flask_login import login_required
from app.charts import bp
import json
import requests
from config import Config
from app.charts.forms import DateForm
from datetime import timedelta, datetime

@bp.route('/', methods=['GET', 'POST'])
# @login_required
def dashboard():
    form = DateForm()
    if form.validate_on_submit():
        start_date = form.start_date.data.strftime('%Y-%m-%d')
        end_date = form.end_date.data.strftime('%Y-%m-%d')
        print(start_date, end_date)
    else:
        yesterday = datetime.today() - timedelta(days=1)
        week_ago = yesterday - timedelta(days=6)

        form.start_date.data = week_ago
        form.end_date.data = yesterday

        start_date = week_ago.strftime('%Y-%m-%d')
        end_date = yesterday.strftime('%Y-%m-%d')

    # Run the cloud function
    url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data"
    payload = {
        "access_token": Config.ACCESS_TOKEN,
        "account_id": "123456789",
        "date_start": start_date,
        "date_end": end_date
        }
    response = requests.get(url, params=payload)
    data = json.loads(response.text)

    spend = sum([float(row['spend']) for row in data])

    return render_template('charts/dashboard.html', title='Dashboard', data=data, spend=spend, form=form)
```

Note it's important we pass the right date format to the form to preload the last 7 days, but also that we have the right date format coming out based on what materialize gives us.

We now need to add the form to the top of the charts page.

```
<div class="row">
    <div class="input-field col s4">
        <h2>Dashboard</h2>
    </div>
    <form action="" method="post">
        {{ form.hidden_tag() }}
        
        <div class="input-field col s3 date-field">
            {{ form.start_date(class_='validate datepicker', type="text") }}
            {{ form.start_date.label() }}
        </div>
        <div class="input-field col s3 date-field">
            {{ form.end_date(class_='validate datepicker', type="text") }}
            {{ form.end_date.label() }}
        </div>
        <div id="run-button" class="col s2 right-align">
            <button type="submit" name="btn" class="waves-effect waves-light btn red">
                RUN QUERY
            </button>
        </div>
    </form>
    

</div>
```

We could do something more fancy with async loading or url params, but for now this will do!

Finally for some styling, add this to the main css file.

```
#run-button {
    margin-top: 4.5em;
}
.date-field {
    margin-top: 4em;
}
```

Now we can work on the account id, which means making the dashboard contigent on a team being selected.

Here's what we need to do:
- store the team id in the session when selected
- display the team name in the navigation bar
- update the Teams model so it has an 'account id'
- rewrite dashboard to take a team parameter
- get the account id for the team when visiting dashboard

Let's do the first one, store the team name and id in the session. To do this we just need to add this to the code in the teams/routes.py.

```
session["team_id"] = team.id
session["team_name"] = team.name
```

Now in the navigation let's display it if it's available. First let's refactor the navigation a little, and fix an issue we have with the dropdown menu not showing on mobile.

First copy the navbar component and put it in a _nav.html file or subtemplate.

Then in base.html replace the nav component with an include.

`{% include "main/_nav.html" %}`

To fix the issue where the navbar dropdown disappears on mobile, change it to this.

```
<!-- Dropdown Trigger -->
<li>
    <a class="dropdown-trigger grey-text hide-on-med-and-down" href="#!" data-target="dropdown">
        Settings<i class="material-icons right">arrow_drop_down</i>
    </a>
    <a class="dropdown-trigger grey-text hide-on-large-only" href="#!" data-target="dropdown">
        <i class="material-icons right">menu</i>
    </a>
</li>
```


Ok now let's write the code for conditionally showing the team when selected.

```
{% if session.team_name %}
<li class="active">
    <a class="grey-text" href="{{ url_for('teams.view_team', team_id=session.team_id) }}">
        <span class="hide-on-large-only">
            <i class="material-icons">supervisor_account</i>
        </span>
        <span class="hide-on-med-and-down">
            <i class="material-icons left">supervisor_account</i>
            {{ session.team_name }}
        </span>
    </a>
</li>
{% else %}
<li>
    <a class="grey-text" href="{{ url_for('teams.list_teams') }}">
        <i class="material-icons left">supervisor_account</i>
        <span class="hide-on-med-and-down">Select Team</span>
    </a>
</li>

{% endif %}
```

If there is a team in the session, we show the team  name and a link to that team. If not, we show a prompt to go to the all teams page and select one there. We made the text in the menu hide on smaller sizes and get replaced by icons on mobile.

Now let's make it so we can save or retrieve an account id from the team. First edit models.py in teams to make it include the account_id.

```
class Team():
    def __init__(self, id_, name, account_id):
        self.id = id_
        self.name = name
        self.account_id = account_id
    
    @staticmethod
    def get(team_id):
        team_data = pyr_db.child('teams').child(team_id).get().val()
        team = Team(
            id_=team_id, 
            name=team_data['name'],
            account_id=team_data.get('account_id')
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
```

Then change the edit route for teams.

```
@bp.route('/<team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):

    role = Membership.user_role(current_user.id, team_id)
    if role not in ["ADMIN", "OWNER"]:
        abort(401, "You don't have access to edit this team.")

    form = TeamForm()

    team = Team.get(team_id)

    if form.validate_on_submit():
        name = form.name.data
        account_id = form.account_id.data

        #edit a team
        try:
            team.update(name, account_id)

            # Update successful
            flash('Team {}, updated with name={}'.format(
                 team.id, team.name), 'teal')

            return redirect(url_for('teams.view_team', team_id=team.id))

        except Exception as e:
            # Update unsuccessful
            flash("Error: {}".format(e), 'red')

    form.name.data = team.name
    form.account_id.data = team.account_id
        
    return render_template('teams/edit_team.html', title='Edit Team', form=form, 
        team=team)
```

In the form add the new field.

```
class TeamForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    account_id = StringField('Account ID')
    submit = SubmitField('SUBMIT')
```

Then in the edit_team.html, add the form field

```
<p class="input-field">
    {{ form.account_id.label }}<br>
    {{ form.account_id(size=32, class_="validate") }}<br>
    {% for error in form.account_id.errors %}
    <span class="helper-text" data-error="[{{ error }}]" data-success=""></span>
    {% endfor %}
</p>
```

Also display the account id in the view_team.html

```
<tr>
    <td>Account ID</td>
    <td>{{ team.account_id }}</td>
</tr>  

```

Now that's working, let's do the final part, which is passing the account_id when loading the dashboard.

Back in charts routes, add these imports
`from flask import render_template, request, flash, redirect, url_for, session, abort`
`from app.teams.models import Team`

Then add this logic to the controller.

```
if not session.get('team_id'):
    # No team selected
    flash("Please select a team", 'orange')
    return redirect(url_for('teams.list_teams'))
else:
    team = Team.get(session.get('team_id'))
    account_id = team.account_id

    if not account_id:
        # No account id for team
        flash("Please update Account ID", 'orange')
        return redirect(url_for('teams.edit_team', team_id=team.id))
```

This kicks the user back to teams if they don't have a team selected, then to edit the team if they don't have an account id.#

Update the running of the cloud function to pass the account_id

```
 # Run the cloud function
url = "https://us-central1-fireflask-ef97c.cloudfunctions.net/get_test_data"
payload = {
    "access_token": Config.ACCESS_TOKEN,
    "account_id": account_id,
    "date_start": start_date,
    "date_end": end_date
    }
response = requests.get(url, params=payload)
data = json.loads(response.text)

spend = sum([float(row['spend']) for row in data])

return render_template('charts/dashboard.html', title='Dashboard', data=data, spend=spend, form=form, account_id=account_id)
```

Let's add a link to the dashboard from the team page
```
<div class="col s6 m3">
    <a href="{{ url_for('charts.dashboard') }}">
        <div class="card-panel">
            Go to dashboard
        </div>
    </a>    
</div>
```

There, we're done with dataviz for now! If an owner doesn't configure an account id and they invite someone to look, they'll get a nasty abort message, which isn't a great user experience - lets make a note to deal with that later on.

Remember to fully implement this we push, merge, push, deploy
`git status`
`git add .`
`git commit -m "finished dataviz"`
`git push`
`git checkout master`
`git pull`
`git merge dataviz`
`git push`

Then over to the other terminal where you have gcloud
`cd C:\Users\Hammer\Documents\Projects\FireFlask\` <!-- only if you changed directories -->
`gcloud config set project fireflask-ef97c` <!-- only if you changed projects -->
`gcloud app deploy`
`gcloud app browse`



