import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # Use SECRET_KEY from environment (.env). If missing, generate a random key at runtime.
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ROOT_PATH = basedir
    STATIC_FOLDER = os.path.join(basedir, 'app//static')
    TEMPLATE_FOLDER_MAIN = os.path.join(basedir, 'app//main//templates')
    TEMPLATE_FOLDER_ERRORS = os.path.join(basedir, 'app//errors//templates')
    TEMPLATE_FOLDER_AUTH = os.path.join(basedir, 'app//auth//templates')
    TEMPLATE_FOLDER_FACULTY = os.path.join(basedir, 'app//faculty//templates')
    TEMPLATE_FOLDER_STUDENT = os.path.join(basedir, 'app//student//templates')
    # Read OAuth values only from environment/.env (no hardcoded fallbacks)
    MICROSOFT_OAUTH_CLIENT_ID = os.environ.get('MICROSOFT_OAUTH_CLIENT_ID')
    MICROSOFT_OAUTH_CLIENT_SECRET = os.environ.get('MICROSOFT_OAUTH_CLIENT_SECRET')
    MICROSOFT_OAUTH_TENANT = os.environ.get('MICROSOFT_OAUTH_TENANT')