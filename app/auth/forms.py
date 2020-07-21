from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=255, 
        message="Password must be 6+ characters")])
    submit = SubmitField('SIGN UP')

class SignInForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('SIGN IN')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('RESET PASSWORD')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    job_title = StringField('Job title')
    photo = FileField('image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('UPDATE')

class UploadPhotoForm(FlaskForm):
    photo = FileField('image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('UPLOAD')

class TeamForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('SUBMIT')

class InviteForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    
    available_roles = ['READ', 'EDIT', 'ADMIN', 'OWNER']
    role_choices = [(role, role) for role in available_roles] # format required by flask wtf

    role = SelectField('Role', choices=role_choices, default='READ', validators=[DataRequired()])
    
    submit = SubmitField('INVITE')