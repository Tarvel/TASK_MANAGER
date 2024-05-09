from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, PasswordField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TaskForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired()])
    task_description = TextAreaField('Task Description', validators=[DataRequired()])
    # due_date = TimeField('Select a date and time', format='%d-%m-%Y %H:%M:%S')
    submit = SubmitField('Submit')

class DeleteForm(FlaskForm):
    delete = SubmitField('Yes')