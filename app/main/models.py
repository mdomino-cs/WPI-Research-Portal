from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin 

profile_major = db.Table(
    'majors',
    db.metadata,
    sqla.Column('profile_id', sqla.Integer, sqla.ForeignKey('profile.user_id'), primary_key=True),
    sqla.Column('major_id', sqla.Integer, sqla.ForeignKey('major.id'), primary_key=True)
)


profile_language = db.Table(
    'languages',
    db.metadata,
    sqla.Column('profile_id', sqla.Integer, sqla.ForeignKey('profile.user_id'), primary_key=True),
    sqla.Column('language_id', sqla.Integer, sqla.ForeignKey('language.id'), primary_key=True)
)

profile_topic = db.Table(
    'student_topics',
    db.metadata,
    sqla.Column('profile_id', sqla.Integer, sqla.ForeignKey('profile.user_id'), primary_key=True),
    sqla.Column('topic_id', sqla.Integer, sqla.ForeignKey('research_topic.id'), primary_key=True)
)

profile_course = db.Table(
    'student_courses',
    db.metadata,
    sqla.Column('profile_id', sqla.Integer, sqla.ForeignKey('profile.user_id'), primary_key=True),
    sqla.Column('course_id', sqla.Integer, sqla.ForeignKey('student_course.id'), primary_key=True)
)

position_major = db.Table(
    'position_majors',
    db.metadata,
    sqla.Column('position_id', sqla.Integer, sqla.ForeignKey('position.id'), primary_key=True),
    sqla.Column('major_id', sqla.Integer, sqla.ForeignKey('major.id'), primary_key=True)
)

position_language = db.Table(
    'position_languages',
    db.metadata,
    sqla.Column('position_id', sqla.Integer, sqla.ForeignKey('position.id'), primary_key=True),
    sqla.Column('language_id', sqla.Integer, sqla.ForeignKey('language.id'), primary_key=True)
)

position_topic = db.Table(
    'position_topics',
    db.metadata,
    sqla.Column('position_id', sqla.Integer, sqla.ForeignKey('position.id'), primary_key=True),
    sqla.Column('topic_id', sqla.Integer, sqla.ForeignKey('research_topic.id'), primary_key=True)
)
position_course = db.Table(
    'position_courses',
    db.metadata,
    sqla.Column('position_id', sqla.Integer, sqla.ForeignKey('position.id'), primary_key=True),
    sqla.Column('course_id', sqla.Integer, sqla.ForeignKey('student_course.id'), primary_key=True)
)

application_user = db.Table(
    'application_user',
    db.metadata,
    sqla.Column('application_id', sqla.Integer, sqla.ForeignKey('applications.id'), primary_key=True),
    sqla.Column('user_id', sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True)
)

user_time_slot = db.Table(
    'user_time_slot',
    db.metadata,
    sqla.Column('user_id', sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True),
    sqla.Column('time_slot_id', sqla.Integer, sqla.ForeignKey('time_slots.id'), primary_key=True)
)

class Major(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), unique=True)

class Language(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), unique=True)

class ResearchTopic(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(128), unique=True)

class User(UserMixin, db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), unique=True, index=True)
    first_name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    last_name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    email : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), unique=True, index=True)
    phone : sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(32), nullable=True)
    password_hash : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(256))
    type = db.Column(db.String(20), nullable=False, default="student")
    microsoft_id : sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(128), unique=True, index=True, nullable=True)

    profile: sqlo.Mapped['Profile'] = sqlo.relationship(
        back_populates='user', uselist=False, cascade='all, delete-orphan'
    )

    times : sqlo.Mapped[Optional[list['TimeSlots']]] = sqlo.relationship(
        secondary=user_time_slot,
        lazy='selectin'
    )

    def __repr__(self):
        return '<User {} - {} - {} - {} - {};>'.format(self.id,self.username,self.email,self.password_hash,self.type)
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    @property
    def role(self):
        """Convenience property to access type as role"""
        return self.type
    
    @role.setter
    def role(self, value):
        """Convenience setter to set type via role"""
        self.type = value
    
    def is_student(self):
        return self.type == 'student'
    
    def is_faculty(self):
        return self.type == 'faculty'

class Applications(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    
    position_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('position.id'))
    
    # 2. CORRECT: student_id references the User table
    student_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('user.id'))
    
    application_date: sqlo.Mapped[datetime] = sqlo.mapped_column(
    sqla.DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    )
    status : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20))
    details : sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.Text, nullable=True)
    reference_requests: sqlo.Mapped[list["ReferenceRequest"]] = sqlo.relationship(
        back_populates="application",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Relationships to resolve ambiguity and provide easy access:
    position: sqlo.Mapped['Position'] = sqlo.relationship(back_populates='applications', foreign_keys=[position_id])
    student: sqlo.Mapped['User'] = sqlo.relationship(foreign_keys=[student_id])

class ReferenceRequest(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)

    application_id: sqlo.Mapped[int] = sqlo.mapped_column(
        sqla.ForeignKey("applications.id"), nullable=False
    )

    faculty_id: sqlo.Mapped[int] = sqlo.mapped_column(
        sqla.ForeignKey("user.id"), nullable=False
    )

    # awaiting | approved | denied
    status: sqlo.Mapped[str] = sqlo.mapped_column(
        sqla.String(20), default="awaiting"
    )

    # simple relations
    application: sqlo.Mapped["Applications"] = sqlo.relationship(
        back_populates="reference_requests"
    )

    faculty: sqlo.Mapped["User"] = sqlo.relationship()


class Position(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    faculty_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('user.id'))
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))
    description : sqlo.Mapped[str] = sqlo.mapped_column(sqla.Text)
    start_date : sqlo.Mapped[datetime] = sqlo.mapped_column(sqla.DateTime(timezone=True))
    end_date : sqlo.Mapped[datetime] = sqlo.mapped_column(sqla.DateTime(timezone=True))
    teamSize : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    minGPA : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float)
    reference : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=False)
    score : sqlo.Mapped[Optional[int]] = sqlo.mapped_column(sqla.Integer, nullable=True)

    majors: sqlo.Mapped[Optional[list[Major]]] = sqlo.relationship(
        secondary=position_major,
        lazy='selectin')


    languages : sqlo.Mapped[Optional[list[Language]]] = sqlo.relationship(
        secondary=position_language,
        lazy='selectin'
    )

    research_topics: sqlo.Mapped[Optional[list['ResearchTopic']]] = sqlo.relationship(
        secondary=position_topic,
        lazy='selectin'
    )

    courses: sqlo.Mapped[Optional[list['StudentCourse']]] = sqlo.relationship(
        secondary=position_course,
        lazy='selectin'
    )
    applications: sqlo.Mapped[list['Applications']] = sqlo.relationship(
        back_populates='position', 
        cascade='all, delete-orphan'
    )

    faculty: sqlo.Mapped['User'] = sqlo.relationship(foreign_keys=[faculty_id])


class Profile(db.Model):

    user_id: sqlo.Mapped[int] = sqlo.mapped_column(
        sqla.ForeignKey('user.id'), primary_key=True
    )
    gpa: sqlo.Mapped[Optional[float]] = sqlo.mapped_column(sqla.Float, nullable=True)

    user: sqlo.Mapped[User] = sqlo.relationship(foreign_keys=[user_id], back_populates='profile')

    majors: sqlo.Mapped[Optional[list[Major]]] = sqlo.relationship(
        secondary=profile_major,
        lazy='selectin')


    languages : sqlo.Mapped[Optional[list[Language]]] = sqlo.relationship(
        secondary=profile_language,
        lazy='selectin'
    )

    research_topics: sqlo.Mapped[Optional[list['ResearchTopic']]] = sqlo.relationship(
        secondary=profile_topic,
        lazy='selectin'
    )

    courses: sqlo.Mapped[Optional[list['StudentCourse']]] = sqlo.relationship(
        secondary=profile_course,
        lazy='selectin'
    )


class StudentCourse(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    course_name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(128))
    grade: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(16), nullable=True)
    instructor: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(128), nullable=True)
    term: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(32), nullable=True)


class TimeSlots(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    time: sqlo.Mapped[datetime] = sqlo.mapped_column(sqla.DateTime(timezone=True), nullable=True)
    faculty_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('user.id'))

    faculty : sqlo.Mapped['User'] = sqlo.relationship(foreign_keys=[faculty_id])

    # Optional link to the application this slot was offered for
    application_id: sqlo.Mapped[Optional[int]] = sqlo.mapped_column(
        sqla.ForeignKey('applications.id'), nullable=True
    )

    # If a student reserves the slot, record their user id
    student_id: sqlo.Mapped[Optional[int]] = sqlo.mapped_column(
        sqla.ForeignKey('user.id'), nullable=True
    )

    # status: available | reserved | cancelled
    status: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20), default='available')

    # convenience relationships
    application: sqlo.Mapped[Optional['Applications']] = sqlo.relationship(foreign_keys=[application_id])
    student: sqlo.Mapped[Optional['User']] = sqlo.relationship(foreign_keys=[student_id])






@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
