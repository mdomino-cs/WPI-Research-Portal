from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, StringField, FloatField, TextAreaField, SubmitField, SelectField, SelectMultipleField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Optional, Length, NumberRange, ValidationError
from app import db
from wtforms.widgets import ListWidget, CheckboxInput
from app.main.models import User


from app.main.models import Major, Language, ResearchTopic, StudentCourse


class ProfileForm(FlaskForm):
	phone = StringField('Phone', validators=[Optional(), Length(max=32)])
	gpa = FloatField('GPA', validators=[Optional(), NumberRange(min=0.0, max=4.0)])
	majors = SelectMultipleField('Majors', coerce=int, validators=[Optional()])
	languages = SelectMultipleField('Languages', coerce=int, validators=[Optional()])
	research_topics = SelectMultipleField('Research Topics', coerce=int, validators=[Optional()])
	submit = SubmitField('Save Profile')


class CourseForm(FlaskForm):
	course_name = SelectField('Course Name', coerce=int, validators=[DataRequired()])
	# Grade and Instructor models don't exist in this schema; accept free-text instead
	grade = StringField('Grade', validators=[Optional(), Length(max=16)])
	instructor = StringField('Instructor', validators=[Optional(), Length(max=128)])
	term = StringField('Term', validators=[Optional(), Length(max=32)])
	submit = SubmitField('Add Course')


class PositionForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(max=100)])
	description = TextAreaField('Description', validators=[DataRequired()])
	start_date = DateField('Start Date (YYYY-MM-DD)', validators=[DataRequired()])
	end_date = DateField('End Date (YYYY-MM-DD)', validators=[DataRequired()])
	teamSize = FloatField('Team Size', validators=[DataRequired(), NumberRange(min=1)])
	minGPA = FloatField('Minimum GPA', validators=[DataRequired(), NumberRange(min=0.0, max=4.0)])
	reference = BooleanField('Reference Required (True/False)')
	majors = QuerySelectMultipleField('Majors', query_factory=lambda: db.session.query(Major).all(), get_label=lambda major: major.name, validators=[Optional()], allow_blank=True, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
	languages = QuerySelectMultipleField('Languages', query_factory=lambda: db.session.query(Language).all(), get_label=lambda language: language.name, validators=[Optional()], allow_blank=True, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
	research_topics = QuerySelectMultipleField('Research Topics', query_factory=lambda: db.session.query(ResearchTopic).all(), get_label=lambda topic: topic.name, validators=[Optional()], allow_blank=True, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
	courses = QuerySelectMultipleField(
		'Courses',
		query_factory=lambda: db.session.query(StudentCourse).all(),
		get_label=lambda course: course.course_name,
		validators=[Optional()],
		allow_blank=True,
		widget=ListWidget(prefix_label=False),
		option_widget=CheckboxInput()
	)
	submit = SubmitField('Create Position')
	
	

class ApplicationForm(FlaskForm):
	details = StringField('Statement Of Interest', validators=[DataRequired(), Length(max=500)])
	# Only include faculty users here
	users = QuerySelectMultipleField(
		'Users',
		query_factory=lambda: db.session.query(User).filter_by(type='faculty').all(),
		get_label=lambda user: f"{user.first_name} {user.last_name}",
		validators=[Optional()],
		allow_blank=True,
		widget=ListWidget(prefix_label=False),
		option_widget=CheckboxInput()
	)
	submit = SubmitField('Submit Application')
