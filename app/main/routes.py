import sys
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sqla
from app import db
from flask_login import current_user, login_required
from datetime import datetime, timezone

from app.main import main_blueprint as bp_main
from .models import User, Profile, StudentCourse, Position, Major, ResearchTopic, Language, Applications, profile_course, ReferenceRequest, TimeSlots
from .forms import PositionForm, ProfileForm, CourseForm, ApplicationForm
import smtplib
import secrets
import os
import requests
import jwt  # PyJWT
import json
from time import time

# Zoom credentials: prefer Server-to-Server OAuth (recommended by Zoom)
ZOOM_CLIENT_ID = os.environ.get('ZOOM_CLIENT_ID')
ZOOM_ACCOUNT_ID = os.environ.get('ZOOM_ACCOUNT_ID')
ZOOM_CLIENT_SECRET = os.environ.get('ZOOM_CLIENT_SECRET')


# create a function to generate a token
# using the pyjwt library


def _get_zoom_access_token():
    """
    Fetch a Zoom access token using Server-to-Server OAuth.
    Falls back to legacy JWT if S2S credentials are not configured.
    """
    if ZOOM_CLIENT_ID and ZOOM_CLIENT_SECRET and ZOOM_ACCOUNT_ID:
        resp = requests.post(
            "https://zoom.us/oauth/token",
            params={"grant_type": "account_credentials", "account_id": ZOOM_ACCOUNT_ID},
            auth=(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET),
            timeout=10,
        )
        if not resp.ok:
            # Make invalid_client more actionable
            if resp.status_code == 400 and "invalid_client" in resp.text:
                raise RuntimeError(
                    "Zoom OAuth token request failed: invalid_client. "
                    "Verify ZOOM_CLIENT_ID/ZOOM_CLIENT_SECRET/ZOOM_ACCOUNT_ID (Production keys) "
                    "and that the Server-to-Server OAuth app is activated."
                )
            raise RuntimeError(f"Zoom OAuth token request failed ({resp.status_code}): {resp.text}")
        data = resp.json()
        token = data.get("access_token")
        if not token:
            raise RuntimeError(f"Zoom OAuth token missing access_token: {data}")
        return token

    # If we reach here, required Zoom credentials are not configured.
    raise RuntimeError("Zoom credentials not configured. Set ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, and ZOOM_ACCOUNT_ID in environment or .env")

def createMeeting(meetingdetails):
    headers = {
        'authorization': 'Bearer ' + _get_zoom_access_token(),
        'content-type': 'application/json'
    }
    r = requests.post(
        'https://api.zoom.us/v2/users/me/meetings',
        headers=headers,
        json=meetingdetails,
        timeout=10,
    )

    # Fail fast with the Zoom error payload if the request was not successful
    if not r.ok:
        raise RuntimeError(f"Zoom meeting creation failed ({r.status_code}): {r.text}")

    try:
        payload = r.json()
    except ValueError:
        raise RuntimeError(f"Zoom meeting creation returned non-JSON: {r.text}")

    join_url = payload.get("join_url")
    start_url = payload.get("start_url")
    meeting_password = payload.get("password")
    if not join_url:
        raise RuntimeError(f"Zoom response missing join_url: {payload}")
    # start_url is host-only and allows starting without being logged into Zoom
    return join_url, start_url, meeting_password



def _get_or_create_profile(user: User) -> Profile:
    profile = user.profile
    if not profile:
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()
    return profile


@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@bp_main.route('/profile', methods=['GET'])
@login_required
def profile_view():
    profile = _get_or_create_profile(current_user)
    courses = current_user.profile.courses or []
    return render_template('display_profile.html', user=current_user, profile=profile, courses=courses)


@bp_main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    profile = _get_or_create_profile(current_user)
    
    majors_list = db.session.scalars(sqla.select(Major).order_by(Major.name)).all()
    languages_list = db.session.scalars(sqla.select(Language).order_by(Language.name)).all()
    topics_list = db.session.scalars(sqla.select(ResearchTopic).order_by(ResearchTopic.name)).all()
    
    
    form = ProfileForm(obj=profile)
    form.majors.choices = [(m.id, m.name) for m in majors_list]
    form.languages.choices = [(l.id, l.name) for l in languages_list]
    form.research_topics.choices = [(t.id, t.name) for t in topics_list]
    
    course_form = CourseForm()
    # provide course templates to the template so the UI can show a dropdown
    # Only treat StudentCourse rows that are NOT associated with any profile as templates
    course_templates = db.session.scalars(
        sqla.select(StudentCourse)
        .outerjoin(profile_course, profile_course.c.course_id == StudentCourse.id)
        .where(profile_course.c.profile_id == None)
        .order_by(StudentCourse.course_name)
    ).all()
    

    if form.validate_on_submit():
        # Save phone on the User model (Profile does not have phone)
        current_user.phone = form.phone.data
        profile.gpa = form.gpa.data
        # assign relationship lists (idempotent)
        selected_major_ids = form.majors.data or []
        profile.majors = [db.session.get(Major, int(mid)) for mid in selected_major_ids if db.session.get(Major, int(mid))]

        selected_topic_ids = form.research_topics.data or []
        profile.research_topics = [db.session.get(ResearchTopic, int(tid)) for tid in selected_topic_ids if db.session.get(ResearchTopic, int(tid))]

        selected_language_ids = form.languages.data or []
        profile.languages = [db.session.get(Language, int(lid)) for lid in selected_language_ids if db.session.get(Language, int(lid))]

        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('main.profile_view'))
    
    if request.method == 'GET':
        # populate phone from User (Profile has no phone attribute)
        form.phone.data = current_user.phone
        # populate form selections from relationship lists
        if profile.majors:
            form.majors.data = [m.id for m in profile.majors]
        if profile.languages:
            form.languages.data = [l.id for l in profile.languages]
        if profile.research_topics:
            form.research_topics.data = [t.id for t in profile.research_topics]

    courses = current_user.profile.courses or []
    return render_template('edit_profile.html', form=form, course_form=course_form, courses=courses, user=current_user, course_templates=course_templates)


@bp_main.route('/profile/course/add', methods=['POST'])
@login_required
def add_course():
    # Use existing StudentCourse template entries (not already linked to profiles) for course names
    courses_list = db.session.scalars(
        sqla.select(StudentCourse)
        .outerjoin(profile_course, profile_course.c.course_id == StudentCourse.id)
        .where(profile_course.c.profile_id == None)
        .order_by(StudentCourse.course_name)
    ).all()

    form = CourseForm()
    form.course_name.choices = [(0, '')] + [(c.id, c.course_name) for c in courses_list]

    if form.validate_on_submit():
        course_obj = db.session.get(StudentCourse, form.course_name.data) if form.course_name.data else None

        # create a new StudentCourse entry (do NOT set id/student_id)
        course = StudentCourse(
            course_name=course_obj.course_name if course_obj else (form.course_name.data or ''),
            # grade and instructor are free-text fields now
            grade=(form.grade.data or '').strip() or None,
            instructor=(form.instructor.data or '').strip() or None,
            term=(form.term.data or '').strip() or None
        )
        db.session.add(course)
        profile = _get_or_create_profile(current_user)
        profile.courses.append(course)
        db.session.commit()
        flash('Course added.', 'success')
    else:
        flash('Please correct errors in the course form.', 'warning')
    return redirect(url_for('main.profile_edit'))


@bp_main.route('/profile/course/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id: int):
    course = db.session.get(StudentCourse, course_id)
    profile = _get_or_create_profile(current_user)
    if not course or course not in profile.courses:
        flash('Course not found.', 'warning')
        return redirect(url_for('main.profile_edit'))
    # remove association and delete the student's course row
    try:
        profile.courses.remove(course)
    except ValueError:
        pass
    db.session.delete(course)
    db.session.commit()
    flash('Course removed.', 'success')
    return redirect(url_for('main.profile_edit'))


@bp_main.route('/positions', methods=['GET'])
@login_required
def positions():
    filter_status = request.args.get('filter', 'relevant')
    query = sqla.select(Position)

    if current_user.is_student() and filter_status == 'applied':
        query = query.join(Applications).where(Applications.student_id == current_user.id)
    if current_user.is_student() and filter_status == 'relevant':
        relevance()
        query = query.order_by(Position.score.desc())   
    if size := request.args.get('team_size'):
        query = query.where(Position.teamSize >= int(size))
    if gpa := request.args.get('min_gpa'):
        query = query.where(Position.minGPA >= float(gpa))
    if start := request.args.get('start_date'):
        query = query.where(Position.start_date >= datetime.strptime(start, '%Y-%m-%d'))
    if end := request.args.get('end_date'):
        query = query.where(Position.end_date <= datetime.strptime(end, '%Y-%m-%d'))

    positions = db.session.scalars(query).all()
    applied_positions = db.session.scalars(
        sqla.select(Position.id)
        .join(Applications)
        .where(Applications.student_id == current_user.id)
    ).all() if current_user.is_student() else []
    return render_template('positions.html', positions=positions, applied_positions=applied_positions)

def relevance():
    profile = current_user.profile
    if not profile:
        return sqla.select(Position).where(sqla.text('0=1'))  # no results
    all_positions = db.session.query(Position).all()

    for position in all_positions:
        score = 0
        # Majors
        if profile.majors and position.majors:
            major_overlap = set(m.id for m in profile.majors).intersection(set(m.id for m in position.majors))
            score += len(major_overlap) * 3  # weight majors higher
        # Research Topics
        if profile.research_topics and position.research_topics:
            topic_overlap = set(t.id for t in profile.research_topics).intersection(set(t.id for t in position.research_topics))
            score += len(topic_overlap) * 2
        # Languages
        if profile.languages and position.languages:
            lang_overlap = set(l.id for l in profile.languages).intersection(set(l.id for l in position.languages))
            score += len(lang_overlap) * 1
        position.score = score
        db.session.commit()

@bp_main.route('/positions/make', methods=['GET', 'POST'])
@login_required
def make_positions():
    pform = PositionForm()
    if pform.validate_on_submit():
        position = Position(
            faculty_id=current_user.id,
            title=pform.title.data.strip(),
            description=pform.description.data.strip(),
            start_date=pform.start_date.data,
            end_date=pform.end_date.data,
            teamSize= pform.teamSize.data,
            minGPA=pform.minGPA.data,
            reference=pform.reference.data,
            majors=pform.majors.data,
            languages=pform.languages.data,
            research_topics=pform.research_topics.data,
            courses=pform.courses.data
        )
        db.session.add(position)
        db.session.commit()
        flash('Position created.', 'success')
        return redirect(url_for('main.positions'))
    return render_template('make_positions.html', form=pform)

@bp_main.route('/positions/<int:position_id>/details', methods=['GET'])
@login_required
def position_details(position_id: int):
    position = db.session.get(Position, position_id)
    references = db.session.scalars(
        sqla.select(ReferenceRequest).join(Applications).where(
            Applications.position_id == position_id,
            Applications.student_id == current_user.id
        )
    ).all()

    if current_user.type == 'student':
        has_applied = db.session.query(Applications).filter_by(
            student_id=current_user.id,
            position_id=position.id
        ).first() is not None
    else:
        has_applied = True

    if not position:
        flash('Position not found.', 'warning')
        return redirect(url_for('main.positions'))
    return render_template('position_details.html', position=position, has_applied=has_applied, references=references)

@bp_main.route('/positions/<int:position_id_>/application', methods=['GET','POST'])
@login_required
def position_application(position_id_: int):

    appForm = ApplicationForm()
    position = db.session.query(Position).where(Position.id == position_id_).first()
    needRef = position.reference

    if appForm.validate_on_submit():
        reference_requests = []
        if needRef:
            for faculty in appForm.users.data:
                reference_request = ReferenceRequest(
                    faculty_id=faculty.id,
                    status='awaiting',
                )
                reference_requests.append(reference_request)

        application = Applications(
            position_id = position_id_,
            student_id = current_user.id,
            application_date = datetime.now(),
            reference_requests=reference_requests,
            status='Pending',
            details=appForm.details.data,
            student = current_user
        )

        db.session.add(application)
        db.session.commit()
        flash('Position applied for')
        return redirect(url_for('main.positions'))
    return render_template('apply.html', form=appForm, needRef=needRef)

@bp_main.route('/applications/<int:app_id>/withdraw', methods=['POST'])
@login_required
def withdraw_application(app_id):
    app = db.session.get(Applications, app_id)
    
    if not app or app.student_id != current_user.id:
        flash('Application not found or unauthorized.', 'warning')
        return redirect(url_for('main.positions', filter='all'))

    if app.status != 'Pending':
        flash('You can only withdraw pending applications.', 'danger')
        return redirect(url_for('main.positions', filter='all'))

    db.session.delete(app)
    db.session.commit()
    flash('Application withdrawn.', 'success')

    return redirect(url_for('main.positions', filter='all'))

@bp_main.route('/inbox', methods=['GET'])
@login_required
def inbox():
    # Placeholder for inbox functionality
    positions = db.session.scalars(sqla.select(Position).where(Position.faculty_id == current_user.id)).all() or None
    applications = db.session.scalars(
        sqla.select(Applications)
        .join(Position)
        .where(Position.faculty_id == current_user.id)
    ).all() or None
    references = db.session.scalars(
        sqla.select(ReferenceRequest).where(ReferenceRequest.faculty_id == current_user.id)
    ).all()
    studentReferences = db.session.scalars(
        sqla.select(ReferenceRequest).join(Applications).where(Applications.student_id == current_user.id)
    ).all() 
    studentInterviews = db.session.scalars(
        sqla.select(Applications).where(Applications.student_id == current_user.id, Applications.status == 'Interview')
    ).all()
    applicationsDenied = db.session.scalars(
    sqla.select(Applications)
        .where(
            Applications.student_id == current_user.id,
            Applications.status == 'Denied'
        )
        .order_by(Applications.application_date.desc())
        .limit(5)
    ).all()

    # For each interview application, show available time slots from the faculty who requested the interview
    slots_by_app = {}
    for app in studentInterviews:
        # Prefer slots explicitly linked to this application (created by the faculty for this app)
        slots = db.session.scalars(
            sqla.select(TimeSlots).where(TimeSlots.application_id == app.id).order_by(TimeSlots.time)
        ).all()
        # Fallback: if none found, show any available slots by the position's faculty
        if not slots and app.position:
            slots = db.session.scalars(
                sqla.select(TimeSlots).where(TimeSlots.faculty_id == app.position.faculty_id, TimeSlots.status == 'available').order_by(TimeSlots.time)
            ).all()
        slots_by_app[app.id] = slots

    return render_template('inbox.html', current_user=current_user, positions=positions, applications=applications, references=references, studentReferences=studentReferences, studentInterviews=studentInterviews, slots_by_app=slots_by_app, applicationsDenied=applicationsDenied)
    

@bp_main.route('/timeslots/<int:slot_id>/accept/<int:app_id>', methods=['POST'])
@login_required
def accept_timeslot(slot_id: int, app_id: int):
    slot = db.session.get(TimeSlots, slot_id)
    application = db.session.get(Applications, app_id)
    if not slot:
        flash('Time slot not found.', 'warning')
        return redirect(url_for('main.inbox'))
    if not application or application.student_id != current_user.id:
        flash('Unauthorized to accept this time slot.', 'danger')
        return redirect(url_for('main.inbox'))

    # ensure the slot belongs to the faculty for this application's position
    if application.position and slot.faculty_id != application.position.faculty_id:
        flash('This time slot is not associated with this application.', 'danger')
        return redirect(url_for('main.inbox'))

    # reserve the slot: mark as reserved and record the student
    if slot.status != 'available':
        flash('This time slot is no longer available.', 'warning')
        return redirect(url_for('main.inbox'))
    slot.student_id = current_user.id
    slot.status = 'reserved'
    scheduled_time = slot.time

    # mark application as Scheduled and save scheduled time in details (human-readable)
    application.status = 'Scheduled'
    application.details = (application.details or '') + f"\nScheduled: {scheduled_time.isoformat()}"
    db.session.commit()

    # Send confirmation emails to both student and faculty
    try:
        # Read email sender credentials from environment
        sender = os.environ.get('EMAIL_SENDER')
        sender_password = os.environ.get('EMAIL_PASSWORD')
        if not sender or not sender_password:
            raise RuntimeError("Email credentials not configured. Set EMAIL_SENDER and EMAIL_PASSWORD in environment or .env")

        faculty = slot.faculty
        student = current_user
        meetingdetails = {
            "topic": f"Interview: {application.position.title}",
            "type": 2,
            "start_time": scheduled_time.astimezone(timezone.utc).isoformat(),
            "duration": "30",
            "timezone": "UTC",
            "agenda": f"Interview for position {application.position.title}",
            "settings": {
                "host_video": True,
                "participant_video": True,
                "join_before_host": False,
                "mute_upon_entry": True,
                "watermark": True,
                "audio": "voip",
                "auto_recording": "cloud",
            },
        }

        meeting_url, start_url, meeting_password = createMeeting(meetingdetails)
        subject_f = "Interview scheduled with student"
        body_f = (
            f"An interview has been scheduled by {student.first_name} {student.last_name} "
            f"for the position '{application.position.title}' on {scheduled_time.isoformat()}.\n\n"
            f"Student email: {student.email}\nApplication ID: {application.id}\n"
            f"Zoom link (host): {start_url or meeting_url}\n"
            f"Join link (participants): {meeting_url}\nPassword: {meeting_password or '[none]'}"
        )
        message_f = f"Subject: {subject_f}\n\n{body_f}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, sender_password)
        server.sendmail(sender, faculty.email, message_f)
        server.quit()

        # Email to student
        subject_s = "Interview confirmed"
        body_s = (
            f"Your interview for position '{application.position.title}' with {faculty.first_name} {faculty.last_name} "
            f"is scheduled for {scheduled_time.isoformat()}.\n\n"
            f"Faculty email: {faculty.email}\nApplication ID: {application.id}\n"
            f"Join link: {meeting_url}\nPassword: {meeting_password or '[none]'}"
        )
        message_s = f"Subject: {subject_s}\n\n{body_s}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, sender_password)
        server.sendmail(sender, student.email, message_s)
        server.quit()
    except Exception as e:
        # don't break the flow if email fails; log and notify user
        print("Failed to send confirmation emails:", e)
        flash('Interview scheduled but confirmation email failed to send.', 'warning')

    flash('Time slot accepted — interview scheduled.', 'success')
    return redirect(url_for('main.inbox'))


@bp_main.route('/applications/<int:app_id>/remove_denied', methods=['POST'])
@login_required
def remove_denied_applications(app_id: int):
    application = db.session.get(Applications, app_id)

    if not application or application.student_id != current_user.id:
        flash('Application not found or unauthorized.', 'warning')
        return redirect(url_for('main.inbox'))

    if application.status != 'Denied':
        flash('Only denied applications can be removed.', 'danger')
        return redirect(url_for('main.inbox'))

    db.session.delete(application)
    db.session.commit()
    flash('Denied application removed.', 'success')

    return redirect(url_for('main.inbox'))

