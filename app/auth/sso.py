import os
from flask import render_template, flash, redirect, url_for, request
from flask_dance.contrib.azure import make_azure_blueprint
from flask_dance.consumer import oauth_authorized
from flask_login import login_user
from app.main.models import User
from app import db

azure_blueprint = make_azure_blueprint(
    client_id=os.environ.get('MICROSOFT_OAUTH_CLIENT_ID'),
    client_secret=os.environ.get('MICROSOFT_OAUTH_CLIENT_SECRET'),
    tenant="common",
    scope=["User.Read", "openid", "email", "profile"],
    redirect_url=os.environ.get('MICROSOFT_OAUTH_REDIRECT_URI')
)

def generate_username(first_name: str, last_name: str) -> str:
    base_username = f"{first_name.lower()}.{last_name.lower()}"
    username = base_username
    counter = 1
    
    while db.session.query(User).filter_by(username=username).first():
        username = f"{base_username}{counter}"
        counter += 1
    
    return username

@oauth_authorized.connect_via(azure_blueprint)
def azure_logged_in(blueprint, token):
    #flash("Executing updated sso.py")  # Debugging message
    if not token:
        flash("No token received from Azure", "danger")
        return redirect(url_for('main.index'))
    
    resp = blueprint.session.get("/v1.0/me")
    if not resp.ok:
        flash("Failed to get user info from Azure", "danger")
        return redirect(url_for('main.index'))
    
    user_info = resp.json()
    email = user_info.get("mail", user_info.get("userPrincipalName")) or "noemail@unknown.com"

    if email.endswith('@wpi.edu'):
        flash("WPI emails are not usable for this site. Please use a personal email.", "danger")
        return redirect(url_for('auth.login'))

    ms_id = user_info.get("id") or "no-id"

    user = User.query.filter_by(microsoft_id=ms_id).first()
    if not user:
        user = User.query.filter_by(email=email).first()
        if user:
            # User exists, link their microsoft_id
            user.microsoft_id = ms_id
            db.session.commit()
            login_user(user)
            flash("Successfully logged in with Microsoft!", "success")
            return redirect(url_for('main.index'))
        else:
            # User does not exist, redirect to registration
            first_name = user_info.get("givenName") or "N/A"
            last_name = user_info.get("surname") or "N/A"
            flash("Your account does not exist. Please register.", "info")
            return redirect(url_for('auth.register', email=email, first_name=first_name, last_name=last_name))
    else:
        # User found by microsoft_id, log them in
        login_user(user)
        flash("Successfully logged in with Microsoft!", "success")
        return redirect(url_for('main.index'))
    
    # Fallback redirect
    return redirect(url_for('main.index'))