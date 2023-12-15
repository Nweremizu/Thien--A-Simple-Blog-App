import os

# Get the current working directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Define the config class
class Config(object):
    # Defines the configuration variables
    # Secret key for the application
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # URI for the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
        # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email server configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25) # 587
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # None
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # None
    ADMINS = ['brunex7900@gmail.com']

    # Pagination
    POSTS_PER_PAGE = 3