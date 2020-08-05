### 11: Visualizing Data

Next up we'll be visualizing our data with chart.js. 

- [https://www.patricksoftwareblog.com/creating-charts-with-chart-js-in-a-flask-application/](https://www.patricksoftwareblog.com/creating-charts-with-chart-js-in-a-flask-application/)
- [https://blog.ruanbekker.com/blog/2017/12/14/graphing-pretty-charts-with-python-flask-and-chartjs/](https://blog.ruanbekker.com/blog/2017/12/14/graphing-pretty-charts-with-python-flask-and-chartjs/)
- [https://towardsdatascience.com/flask-and-chart-js-tutorial-i-d33e05fba845](https://towardsdatascience.com/flask-and-chart-js-tutorial-i-d33e05fba845)

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



Our users will expect to see the ability to choose date range and client / team, so we need to make it more dynamic. This will mean changes to our cloud function to support this.

