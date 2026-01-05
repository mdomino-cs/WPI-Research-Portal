from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import db
from app.auth import auth 
import sqlalchemy as sqla
from flask_login import login_user, current_user, logout_user, login_required
import smtplib
from itsdangerous import URLSafeTimedSerializer

from app.auth.auth_forms import RegistrationForm, LoginForm, LoginFacultyForm
from app.main.models import User


SECRET_KEY = "my-hardcoded-secret-1234"


@auth.route('/user/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    email = request.args.get('email')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    regForm = RegistrationForm(email=email, first_name=first_name, last_name=last_name)

    if regForm.validate_on_submit():
        if User.query.filter_by(email=regForm.email.data).first() and User.query.filter_by(username=regForm.username.data).first():
            flash('Both Username and Email already registered. Please use a different username and email.')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(username=regForm.username.data).first():
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=regForm.email.data).first():
            flash('Email already registered. Please use a different email.')
            return redirect(url_for('auth.register'))
        user = User(username=regForm.username.data,first_name=regForm.first_name.data,last_name=regForm.last_name.data,email=regForm.email.data)

        user.set_password(regForm.password.data)

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('You are now a user')
        return redirect(url_for('main.index'))
    return render_template('register.html',form=regForm)

@auth.route('/user/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    lform = LoginForm()
    if lform.validate_on_submit():
        query = sqla.select(User).where(User.username == lform.username.data)
        user = db.session.scalars(query).first()

        if (user is None) or (user.check_password(lform.password.data) == False):
            return redirect(url_for('auth.login'))
        
        login_user(user,remember=lform.remember_me.data)
        flash('The user has succesfully loggin in!!')
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html',form=lform)


@auth.route('/faculty/login', methods=['GET', 'POST'])
def login_faculty():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginFacultyForm()

    if form.validate_on_submit():
        user = form.faculty_user.data  # This is already a User object

        # Check password
        if not user.check_password(form.password.data):
            flash("Invalid password.", "danger")
            return redirect(url_for('auth.login_faculty'))
        
        # Generate token
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        token = serializer.dumps(user.email, salt='email-login')

        # Create link
        link = url_for('auth.confirm_login', token=token, _external=True)
        message = f"Subject: Log in link\n\nClick this link to log in: {link}"


        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("michaeld8866@gmail.com", "pokf tyrc johk toba")
        server.sendmail("michaeld8866@gmail.com", user.email,message)
        server.quit()

        flash("A login link has been sent to your email.", "info")
        return redirect(url_for('auth.login_faculty'))
        login_user(user)
        flash("You are now logged in!", "success")
        return redirect(url_for('main.index'))
    return render_template('faculty_login.html', form=form)

@auth.route('/confirm_login/<token>')
def confirm_login(token):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt='email-login', max_age=3600)  # 1 hour expiry
    except:
        flash("The link is invalid or expired.", "danger")
        return redirect(url_for('auth.login_faculty'))

    user = User.query.filter_by(email=email).first_or_404()
    login_user(user)
    flash("You are now logged in!", "success")
    return redirect(url_for('main.index'))

@auth.route('/user/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))