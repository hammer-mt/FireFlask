from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class TeamForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    account_id = StringField('Account ID')
    conversion_event = StringField('Conversion Event')
    submit = SubmitField('SUBMIT')

class InviteForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    
    available_roles = ['READ', 'EDIT', 'ADMIN']
    role_choices = [(role, role) for role in available_roles] # format required by flask wtf

    role = SelectField('Role', choices=role_choices, default='READ', validators=[DataRequired()])
    
    submit = SubmitField('INVITE')