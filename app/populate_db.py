"""Database population script for local development.

Run this from the project root (where `termProject.py` / `app` package lives) like:

    python -m app.populate_db

It is idempotent: it will check for existing rows before creating duplicates.
"""
from datetime import datetime, timezone, timedelta
from app import create_app, db
from app.main.models import (
    Major, Language, ResearchTopic, User, Profile, StudentCourse, Position, Applications
)

app = create_app()

SAMPLE_MAJORS = [
    "CS",
    "MA",
    "ECE",
    "DS",
    "PH",
    "CE"
]

SAMPLE_LANGUAGES = [
    "Python",
    "C++",
    "JavaScript",
    "Java",
    "MATLAB",
]

SAMPLE_TOPICS = [
    "Machine Learning",
    "Computer Vision",
    "Robotics",
    "Natural Language Processing",
    "Embedded Systems",
]

SAMPLE_COURSES = [
    {"course_name": "CS101 - Intro to CS", "grade": "A", "instructor": "Prof. A", "term": "Fall 2024"},
    {"course_name": "CS250 - Data Structures", "grade": "A-", "instructor": "Prof. B", "term": "Spring 2025"},
    {"course_name": "MA200 - Discrete Math", "grade": "B+", "instructor": "Prof. C", "term": "Fall 2024"},
]

FACULTY = [
    {"username": "sjones", "first_name": "Sam", "last_name": "Jones", "email": "sjones@wpi.edu", "password": "password"},
    {"username": "adoe", "first_name": "Alice", "last_name": "Doe", "email": "adoe@wpi.edu", "password": "password"},
]

STUDENTS = [
    {"username": "student1", "first_name": "John", "last_name": "Smith", "email": "john.smith@example.com", "password": "password", "gpa": 3.6},
    {"username": "student2", "first_name": "Mary", "last_name": "Johnson", "email": "mary.j@example.com", "password": "password", "gpa": 3.9},
]

POSITIONS = [
    {
        "title": "ML Research Assistant",
        "description": "Work on ML experiments and data pipelines",
        "teamSize": 2,
        "minGPA": 3.2,
        "reference": False,
        # will attach majors/languages/topics by names
        "majors": ["Computer Science", "Data Science"],
        "languages": ["Python"],
        "topics": ["Machine Learning"],
        "courses": ["CS250 - Data Structures"]
    },
    {
        "title": "Embedded Systems TA",
        "description": "Work on low-level firmware and sensors",
        "teamSize": 1,
        "minGPA": 3.0,
        "reference": True,
        "majors": ["Electrical and Computer Engineering"],
        "languages": ["C++"],
        "topics": ["Embedded Systems"],
        "courses": ["CS101 - Intro to CS"]
    }
]


def get_or_create(model, defaults=None, **kwargs):
    obj = model.query.filter_by(**kwargs).first()
    if obj:
        return obj, False
    params = dict(**kwargs)
    if defaults:
        params.update(defaults)
    obj = model(**params)
    db.session.add(obj)
    return obj, True


with app.app_context():
    print("Seeding majors/languages/topics...")
    created = []
    for name in SAMPLE_MAJORS:
        m, new = get_or_create(Major, name=name)
        created.append((m, new))

    for name in SAMPLE_LANGUAGES:
        l, new = get_or_create(Language, name=name)
        created.append((l, new))

    for name in SAMPLE_TOPICS:
        t, new = get_or_create(ResearchTopic, name=name)
        created.append((t, new))

    db.session.commit()
    print("Committed majors/languages/topics")

    # create faculty
    print("Seeding faculty users...")
    faculty_objs = []
    for f in FACULTY:
        user = User.query.filter_by(email=f["email"]).first()
        if not user:
            user = User(
                username=f["username"],
                first_name=f["first_name"],
                last_name=f["last_name"],
                email=f["email"],
                type='faculty'
            )
            user.set_password(f["password"])
            db.session.add(user)
            db.session.commit()
        faculty_objs.append(user)

    # create students and profiles and courses
    print("Seeding students, profiles, and courses...")
    student_objs = []
    for s in STUDENTS:
        user = User.query.filter_by(email=s["email"]).first()
        if not user:
            user = User(
                username=s["username"],
                first_name=s["first_name"],
                last_name=s["last_name"],
                email=s["email"],
                type='student'
            )
            user.set_password(s["password"])
            db.session.add(user)
            db.session.commit()
        # ensure profile
        if not getattr(user, 'profile', None):
            profile = Profile(user_id=user.id, gpa=s.get('gpa'))
            db.session.add(profile)
            db.session.commit()
        student_objs.append(user)

    # create or get courses (idempotent)
    course_objs = []
    for c in SAMPLE_COURSES:
        course = StudentCourse.query.filter_by(course_name=c['course_name']).first()
        if not course:
            course = StudentCourse(**c)
            db.session.add(course)
            db.session.commit()
        course_objs.append(course)

    # associate first student with first two majors and languages and topics
    print("Associating majors/languages/topics to student profiles...")
    cs_major = Major.query.filter_by(name="Computer Science").first()
    ds_major = Major.query.filter_by(name="Data Science").first()
    python_lang = Language.query.filter_by(name="Python").first()
    ml_topic = ResearchTopic.query.filter_by(name="Machine Learning").first()

    st = student_objs[0]
    if cs_major and cs_major not in st.profile.majors:
        st.profile.majors.append(cs_major)
    if ds_major and ds_major not in st.profile.majors:
        st.profile.majors.append(ds_major)
    if python_lang and python_lang not in st.profile.languages:
        st.profile.languages.append(python_lang)
    if ml_topic and ml_topic not in st.profile.research_topics:
        st.profile.research_topics.append(ml_topic)
    db.session.commit()

    # create positions for faculty
    print("Creating positions for faculty...")
    base_date = datetime.now(timezone.utc)
    pos_objs = []
    for i, p in enumerate(POSITIONS):
        faculty = faculty_objs[i % len(faculty_objs)]
        # Try to find an existing position for this faculty with same title
        pos = Position.query.filter_by(title=p['title'], faculty_id=faculty.id).first()
        if pos:
            # update scalar fields in case they changed
            pos.description = p['description']
            pos.start_date = base_date + timedelta(days=7)
            pos.end_date = base_date + timedelta(days=120)
            pos.teamSize = p['teamSize']
            pos.minGPA = p['minGPA']
            pos.reference = p['reference']
        else:
            pos = Position(
                faculty_id=faculty.id,
                title=p['title'],
                description=p['description'],
                start_date=base_date + timedelta(days=7),
                end_date=base_date + timedelta(days=120),
                teamSize=p['teamSize'],
                minGPA=p['minGPA'],
                reference=p['reference']
            )
            db.session.add(pos)

        # attach many-to-many relationships idempotently
        for mname in p.get('majors', []):
            m = Major.query.filter_by(name=mname).first()
            if m and m not in pos.majors:
                pos.majors.append(m)
        for lname in p.get('languages', []):
            l = Language.query.filter_by(name=lname).first()
            if l and l not in pos.languages:
                pos.languages.append(l)
        for tname in p.get('topics', []):
            t = ResearchTopic.query.filter_by(name=tname).first()
            if t and t not in pos.research_topics:
                pos.research_topics.append(t)
        for cname in p.get('courses', []):
            c = StudentCourse.query.filter_by(course_name=cname).first()
            if c and c not in pos.courses:
                pos.courses.append(c)

        db.session.commit()
        pos_objs.append(pos)

    # create one application from student1 to first position
    print("Creating sample application...")
    if pos_objs and student_objs:
        app_exists = Applications.query.filter_by(position_id=pos_objs[0].id, student_id=student_objs[0].id).first()
        if not app_exists:
            application = Applications(
                position_id=pos_objs[0].id,
                student_id=student_objs[0].id,
                status='submitted',
                details='I am very interested in this position.'
            )
            db.session.add(application)
            db.session.commit()

    print("Database population complete.")
