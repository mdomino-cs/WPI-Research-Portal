from app.decorators import role_required
from app.faculty import faculty_bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main.models import Position, Applications, ReferenceRequest, TimeSlots
from app.faculty.faculty_forms import PositionForm, TimeSlotsForm
from app.main.models import Profile, StudentCourse
from app.main.routes import _get_or_create_profile
from app.faculty.faculty_forms import CourseFormFaculty
import sqlalchemy as sqla


@faculty_bp.route('/faculty/dashboard')
@role_required('faculty')
def dashboard():
    """Faculty dashboard showing their positions."""
    positions = Position.query.filter_by(faculty_id=current_user.id).all()
    return render_template('dashboard.html', positions=positions)


@faculty_bp.route('/faculty/position/create', methods=['GET', 'POST'])
@role_required('faculty')
def create_position():
    """Create a new research position."""
    form = PositionForm()
    
    if form.validate_on_submit():

        if form.end_date.data < form.start_date.data:
            flash('End date cannot be earlier than start date.', 'danger')
            return render_template('create_position.html', form=form)
        
        position = Position(
            faculty_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            teamSize=form.teamSize.data,
            minGPA=form.minGPA.data,
            reference=form.reference.data,
            majors=form.majors.data,
            languages=form.languages.data,
            research_topics=form.research_topics.data,
            courses=form.courses.data
        )

        db.session.add(position)
        db.session.commit()
        flash(f'Position "{position.title}" created successfully!', 'success')
        return redirect(url_for('faculty.dashboard'))
    return render_template('create_position.html', form=form)


@faculty_bp.route('/position/<int:position_id>/edit', methods=['GET', 'POST'])
@role_required('faculty')
def edit_position(position_id):
    """Edit an existing position."""
    position = Position.query.get_or_404(position_id)
    
    # Ensure faculty can only edit their own positions
    if position.faculty_id != current_user.id:
        flash('You can only edit your own positions.', 'danger')
        return redirect(url_for('main.positions'))
    
    form = PositionForm(obj=position)
    if request.method == 'GET':
        # Position model uses research_topics relationship; map it to the form's research_topics field
        form.research_topics.data = position.research_topics
    
    if form.validate_on_submit():
        position.title = form.title.data
        position.description = form.description.data
        position.start_date = form.start_date.data
        position.end_date = form.end_date.data
        position.teamSize = form.teamSize.data
        position.minGPA = form.minGPA.data
        position.reference = form.reference.data
        position.majors = form.majors.data
        position.languages = form.languages.data
        position.research_topics = form.research_topics.data
        db.session.commit()
        flash(f'Position "{position.title}" updated successfully!', 'success')
        return redirect(url_for('main.positions'))
    
    return render_template('edit_position.html', form=form, position=position)


@faculty_bp.route('/position/<int:position_id>/delete', methods=['POST'])
@role_required('faculty')
def delete_position(position_id):
    position = Position.query.get_or_404(position_id)
    
    if position.faculty_id != current_user.id:
        flash('You can only delete your own positions.', 'danger')
        return redirect(url_for('main.positions'))
    
    title = position.title
    db.session.delete(position)
    db.session.commit()
    flash(f'Position "{title}" deleted successfully.', 'success')
    return redirect(url_for('main.positions'))

@faculty_bp.route('/positions/pending')
@role_required('faculty')
def pending_applications():
    positions = Position.query.filter_by(faculty_id=current_user.id).all()
    pending_apps = []
    for position in positions:
        for application in position.applications:
            if application.status == 'Pending':
                pending_apps.append(application)
    return render_template('pending.html', applications=pending_apps)



@faculty_bp.route('/application/<int:app_id>/deny', methods=['POST'])
@role_required('faculty')
def deny_application(app_id: int):
    application = db.session.get(Applications, app_id)

    application.status = 'Denied'
    db.session.commit()
    flash('Application denied.', 'success')
    return redirect(url_for('faculty.pending_applications'))

@faculty_bp.route('/application/<int:app_id>/interview', methods=['GET', 'POST'])
@role_required('faculty')
def interview_application(app_id: int):
    """If GET: show availability form for faculty to add time(s).
       If POST: validate form, create TimeSlots entry, mark application as Interview and return.
    """
    application = db.session.get(Applications, app_id)
    if not application:
        flash('Application not found.', 'danger')
        return redirect(url_for('faculty.pending_applications'))

    form = TimeSlotsForm()

    # existing slots for this application (created by this faculty)
    existing_slots = db.session.scalars(
        sqla.select(TimeSlots)
        .where(TimeSlots.application_id == application.id, TimeSlots.faculty_id == current_user.id)
        .order_by(TimeSlots.time)
    ).all()

    if form.validate_on_submit():
        # combine date + start_time into a timezone-aware datetime and save
        from datetime import datetime, timezone
        dt_start = datetime.combine(form.date.data, form.start_time.data)
        dt_start = dt_start.replace(tzinfo=timezone.utc)

        slot = TimeSlots(time=dt_start, faculty_id=current_user.id, application_id=application.id)
        db.session.add(slot)

        # mark application as Interview and commit
        application.status = 'Interview'
        db.session.commit()
        flash('Availability saved. Add more slots or click Done when finished.', 'success')
        return redirect(url_for('faculty.interview_application', app_id=application.id))

    # GET -> render the form and list of existing slots so faculty can add multiple
    return render_template('new_timeslot.html', form=form, application=application, existing_slots=existing_slots)


@faculty_bp.route('/application/<int:app_id>/timeslot/<int:slot_id>/delete', methods=['POST'])
@role_required('faculty')
def delete_timeslot(app_id: int, slot_id: int):
    application = db.session.get(Applications, app_id)
    slot = db.session.get(TimeSlots, slot_id)
    if not application or not slot:
        flash('Application or timeslot not found.', 'warning')
        return redirect(url_for('faculty.pending_applications'))
    if slot.faculty_id != current_user.id:
        flash('Unauthorized to delete this timeslot.', 'danger')
        return redirect(url_for('faculty.pending_applications'))
    db.session.delete(slot)
    db.session.commit()
    flash('Time slot deleted.', 'success')
    return redirect(url_for('faculty.interview_application', app_id=app_id))

@faculty_bp.route('/application/<int:app_id>/approve', methods=['POST'])
@role_required('faculty')
def approve_application(app_id: int):
    application = db.session.get(Applications, app_id)
    position = application.position

    team_size = position.teamSize
    if team_size and team_size > 0:
        approved_count = db.session.query(Applications).filter(
            Applications.position_id == position.id,
            Applications.status == 'Approved'
        ).count()

        if approved_count >= int(team_size):
            flash('Cannot approve — position already has the maximum number of approved applicants.', 'warning')
            return redirect(url_for('faculty.pending_applications'))

    for reference in application.reference_requests:
        db.session.delete(reference)

    # Approve and commit
    application.status = 'Approved'
    db.session.commit()
    flash('Application approved.', 'success')
    return redirect(url_for('faculty.pending_applications'))

@faculty_bp.route('/application/<int:app_id>/profile', methods=['GET'])
@role_required('faculty')
def profile_view(app_id: int):
    application = db.session.get(Applications, app_id)
    profile = _get_or_create_profile(application.student)
    courses = application.student.profile.courses or []
    return render_template('display_profile.html', user=application.student, profile=profile, courses=courses)

@faculty_bp.route('/application/<int:app_id>/profile', methods=['GET'])
@role_required('faculty')
def profile_view_(app_id: int):
    application = db.session.get(Applications, app_id)
    profile = _get_or_create_profile(application.student)
    courses = application.student.profile.courses or []
    return render_template('display_profile.html', user=application.student, profile=profile, courses=courses)

@faculty_bp.route('/reference/<int:ref_id>/approve', methods=['POST'])
@role_required('faculty')
def approve_reference(ref_id: int):
    reference = db.session.get(ReferenceRequest, ref_id)
    reference.status = 'approved'
    db.session.commit()
    flash('Reference approved.', 'success')
    return redirect(url_for('main.inbox'))

@faculty_bp.route('/reference/<int:ref_id>/deny', methods=['POST'])
@role_required('faculty')
def deny_reference(ref_id: int):
    reference = db.session.get(ReferenceRequest, ref_id)
    reference.status = 'denied'
    db.session.commit()
    flash('Reference denied.', 'success')
    return redirect(url_for('main.inbox'))

@faculty_bp.route('/addData', methods=['GET'])
@role_required('faculty')
def add_data():
    return render_template('addData.html')

@faculty_bp.route('/addData/addCourse', methods=['GET','POST'])
@role_required('faculty')
def add_course():
    form = CourseFormFaculty()
    if form.validate_on_submit():
        course_name = form.course_name.data

        exists = db.session.execute(
            sqla.select(db.exists().where(StudentCourse.course_name == course_name))
        ).scalar()

        if exists:
            flash('Course already exists.', 'warning')
        else:
            course = StudentCourse(course_name=course_name, instructor=current_user.first_name)
            db.session.add(course)
            db.session.commit()
            flash(f'Course "{course_name}" added successfully!', 'success')
            return redirect(url_for('faculty.add_course'))
    return render_template('add_course.html', form=form, courses=StudentCourse.query.all())

@faculty_bp.route('/addData/deleteCourse/<int:course_id>', methods=['POST'])
@role_required('faculty')
def delete_course(course_id: int):
    course = db.session.get(StudentCourse, course_id)
    if course:
        db.session.delete(course)
        db.session.commit()
        flash(f'Course "{course.course_name}" deleted successfully!', 'success')
    else:
        flash('Course not found.', 'danger')
    return redirect(url_for('faculty.add_course'))

@faculty_bp.route('/addData/editCourse/<int:course_id>', methods=['POST'])
@role_required('faculty')
def edit_course(course_id: int):
    course = db.session.get(StudentCourse, course_id)
    form = CourseFormFaculty(obj=course)
    if form.validate_on_submit():
        course.course_name = form.course_name.data
        course.grade = form.grade.data
        course.instructor = form.instructor.data
        course.term = form.term.data
        db.session.commit()
        flash(f'Course "{course.course_name}" updated successfully!', 'success')
        return redirect(url_for('faculty.add_course'))
    return render_template('edit_course.html', form=form, course=course)

@faculty_bp.route('/addData/addLanguage', methods=['GET','POST'])
@role_required('faculty')
def add_language():
    from app.faculty.faculty_forms import LanguageForm
    from app.main.models import Language
    form = LanguageForm()
    if form.validate_on_submit():
        language_name = form.name.data

        exists = db.session.execute(
            sqla.select(db.exists().where(Language.name == language_name))
        ).scalar()

        if exists:
            flash('Language already exists.', 'warning')
        else:
            language = Language(name=language_name)
            db.session.add(language)
            db.session.commit()
            flash(f'Language "{language_name}" added successfully!', 'success')
            return redirect(url_for('faculty.add_language'))
    return render_template('add_language.html', form=form, languages=Language.query.all())

@faculty_bp.route('/addData/deleteLanguage/<int:language_id>', methods=['POST'])
@role_required('faculty')
def delete_language(language_id: int):
    from app.main.models import Language
    language = db.session.get(Language, language_id)
    if language:
        db.session.delete(language)
        db.session.commit()
        flash(f'Language "{language.name}" deleted successfully!', 'success')
    else:
        flash('Language not found.', 'danger')
    return redirect(url_for('faculty.add_language'))

@faculty_bp.route('/addData/addTopic', methods=['GET','POST'])
@role_required('faculty')
def add_topic():
    from app.faculty.faculty_forms import TopicForm
    from app.main.models import ResearchTopic
    form = TopicForm()
    if form.validate_on_submit():
        topic_name = form.name.data

        exists = db.session.execute(
            sqla.select(db.exists().where(ResearchTopic.name == topic_name))
        ).scalar()

        if exists:
            flash('Research Topic already exists.', 'warning')
        else:
            topic = ResearchTopic(name=topic_name)
            db.session.add(topic)
            db.session.commit()
            flash(f'Research Topic "{topic_name}" added successfully!', 'success')
            return redirect(url_for('faculty.add_topic'))
    return render_template('add_topic.html', form=form, topics=ResearchTopic.query.all())

@faculty_bp.route('/addData/deleteTopic/<int:topic_id>', methods=['POST'])
@role_required('faculty')
def delete_topic(topic_id: int):
    from app.main.models import ResearchTopic
    topic = db.session.get(ResearchTopic, topic_id)
    if topic:
        db.session.delete(topic)
        db.session.commit()
        flash(f'Research Topic "{topic.name}" deleted successfully!', 'success')
    else:
        flash('Research Topic not found.', 'danger')
    return redirect(url_for('faculty.add_topic'))

@faculty_bp.route('/addData/editTopic/<int:topic_id>', methods=['POST'])
@role_required('faculty')
def edit_topic(topic_id: int):
    from app.main.models import ResearchTopic
    from app.faculty.faculty_forms import TopicForm
    topic = db.session.get(ResearchTopic, topic_id)
    form = TopicForm(obj=topic)
    if form.validate_on_submit():
        topic.name = form.name.data
        db.session.commit()
        flash(f'Research Topic "{topic.name}" updated successfully!', 'success')
        return redirect(url_for('faculty.add_topic'))
    return render_template('edit_topic.html', form=form, topic=topic)

@faculty_bp.route('/addData/editLanguage/<int:language_id>', methods=['POST'])
@role_required('faculty')
def edit_language(language_id: int):
    from app.main.models import Language
    from app.faculty.faculty_forms import LanguageForm
    language = db.session.get(Language, language_id)
    form = LanguageForm(obj=language)
    if form.validate_on_submit():
        language.name = form.name.data
        db.session.commit()
        flash(f'Language "{language.name}" updated successfully!', 'success')
        return redirect(url_for('faculty.add_language'))
    return render_template('edit_language.html', form=form, language=language)

