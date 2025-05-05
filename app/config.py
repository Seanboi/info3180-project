import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env if it exists.

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')  # Use absolute path
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False