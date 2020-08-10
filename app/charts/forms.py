from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import DateField

class DateForm(FlaskForm):
    start_date = DateField('Start Date', format='%b %d, %Y')
    end_date = DateField('End Date', format='%b %d, %Y')
    submit = SubmitField('RUN QUERY')