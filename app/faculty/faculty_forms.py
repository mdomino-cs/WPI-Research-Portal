from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, IntegerField, FloatField, DateField, TimeField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, NumberRange, Optional, Length

from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from app import db
from wtforms.widgets import ListWidget, CheckboxInput
from app.main.models import Language, Major, ResearchTopic, StudentCourse


class PositionForm(FlaskForm):
    title = StringField('Position Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()],
                                description='Describe the research project and responsibilities')
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    teamSize = IntegerField('Team Size', validators=[DataRequired(), NumberRange(min=1)],
                           description='Number of students needed')
    minGPA = FloatField('Minimum GPA', validators=[DataRequired(), NumberRange(min=0.0, max=4.0)])
    reference = BooleanField('Reference Required')
    majors = QuerySelectMultipleField('Majors', query_factory=lambda: db.session.query(Major).all(), get_label=lambda major: major.name, validators=[Optional()], allow_blank=True, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    languages = QuerySelectMultipleField('Languages', query_factory=lambda: db.session.query(Language).all(), get_label=lambda language: language.name, validators=[Optional()], allow_blank=True, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    research_topics = QuerySelectMultipleField('Research Topics', query_factory=lambda: db.session.query(ResearchTopic).all(), get_label=lambda topic: topic.name, validators=[Optional()], allow_blank=True, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    courses = QuerySelectMultipleField(
    'Courses',
    query_factory=lambda: db.session.query(StudentCourse).all(),
    get_label=lambda course: course.name,
    validators=[Optional()],
    allow_blank=True,
    widget=ListWidget(prefix_label=False),
    option_widget=CheckboxInput()
    )
    submit = SubmitField('Save Position')

    def validate_end_date(self, field):
        if self.start_date.data and field.data:
            if field.data < self.start_date.data:
                raise ValidationError("End date cannot be before start date.")

class CourseFormFaculty(FlaskForm):
	course_name = StringField('Course Name', validators=[DataRequired()])
	# Grade and Instructor models don't exist in this schema; accept free-text instead
	grade = StringField('Grade', validators=[Optional(), Length(max=16)])
	instructor = StringField('Instructor', validators=[Optional(), Length(max=128)])
	term = StringField('Term', validators=[Optional(), Length(max=32)])
	submit = SubmitField('Add Course')
      
class LanguageForm(FlaskForm):
    name = StringField('Language Name', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Add Language')

class TopicForm(FlaskForm):
    name = StringField('Research Topic Name', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Add Research Topic')

class TimeSlotsForm(FlaskForm):
    # Let faculty pick a specific date and start/end times on that date.
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d', description='Select the date for the time slot')
    start_time = TimeField('Start Time', validators=[DataRequired()], format='%H:%M', description='Start time (24-hour HH:MM)')
    submit = SubmitField('Add Time Slot')
