from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email
import sqlalchemy as sqla
from app import db
from app.main.models import User
import re
from wtforms_sqlalchemy.fields import QuerySelectField

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', 
                               validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register')



class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Login")

def faculty_query():
    return User.query.filter_by(type='faculty')

class LoginFacultyForm(FlaskForm):
    faculty_user = QuerySelectField(
        'Faculty Account',
        query_factory=faculty_query,
        get_label=lambda user: f"{user.first_name} {user.last_name}",
        allow_blank=False,
        validators=[DataRequired()]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
