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
