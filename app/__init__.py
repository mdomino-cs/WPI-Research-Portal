from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
moment = Moment()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def seed_faculty():
    from app.main.models import User
    faculty = [
        {
            'first_name': 'Mike',
            'last_name': 'Domino',
            'email': 'mfdomino@wpi.edu',
            'username': 'mike_faculty',
            'password': 'password123',
            'type': 'faculty'
        },
        {
            'first_name': 'Chris',
            'last_name': 'Faculty',
            'email': 'chris@example.com',
            'username': 'chris_faculty',
            'password': 'password123',
            'type': 'faculty'
        }
    ]

    for f in faculty:
        exists = User.query.filter_by(email=f['email']).first()

        if not exists:
            user = User(
                username=f['username'],
                first_name=f['first_name'],
                last_name=f['last_name'],
                email=f['email'],
                type=f['type']
            )
            user.set_password(f['password'])
            db.session.add(user)

    db.session.commit()

def seed_courses():
    """Seed reusable course templates for faculty/student selection."""
    from app.main.models import StudentCourse
    courses = [
        'CS1004 - Intro to Programming',
        'CS2011 - Intro to Machine Organization',
        'CS2022 - Discrete Math',
        'CS2102 - Object-Oriented Design',
        'CS2223 - Algorithms',
        'CS3013 - Operating Systems',
        'CS3431 - Database Systems',
        'CS3733 - Software Engineering',
        'CS4120 - Analysis of Algorithms',
        'CS4341 - Artificial Intelligence',
        'CS4342 - Machine Learning',
        'CS4513 - Distributed Systems',
        'MA1021 - Calculus I',
        'MA1022 - Calculus II',
        'MA1023 - Calculus III',
        'MA2024 - Calculus IV',
        'MA2071 - Matrices and Linear Algebra'
    ]
    
    for course_name in courses:
        exists = StudentCourse.query.filter_by(course_name=course_name).first()
        if not exists:
            course = StudentCourse(course_name=course_name)
            db.session.add(course)
    
    db.session.commit()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER_MAIN

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.config["PREFERRED_URL_SCHEME"] = "https"

    db.init_app(app)

    from app.main.models import User

    

    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    from app.main import main_blueprint as main
    main.template_folder = Config.TEMPLATE_FOLDER_MAIN
    app.register_blueprint(main)

    from app.auth import auth
    auth.template_folder = Config.TEMPLATE_FOLDER_AUTH
    app.register_blueprint(auth, url_prefix='/auth')

    from app.auth.sso import azure_blueprint
    app.register_blueprint(azure_blueprint, url_prefix='/login')

    from app.errors import error_blueprint as errors
    errors.template_folder = Config.TEMPLATE_FOLDER_ERRORS
    app.register_blueprint(errors)

    from app.student import student_bp
    from app.faculty import faculty_bp
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(faculty_bp, url_prefix='/faculty')

    return app
