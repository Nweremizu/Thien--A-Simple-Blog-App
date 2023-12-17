import os

# Get the current working directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Define the config class
class Config(object, ):
    # Defines the configuration variables
    # Secret key for the application
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Database configuration
    DB_ENGINE = os.getenv('DB_ENGINE', None)
    DB_USERNAME = os.getenv('DB_USERNAME', None)
    DB_PASS = os.getenv('DB_PASS', None)
    DB_HOST = os.getenv('DB_HOST', None)
    DB_NAME = os.getenv('DB_NAME', None)
    
    USE_SQLITE = True
    
    if DB_ENGINE and DB_NAME and DB_USERNAME:
            try:

                # Relational DBMS: PSQL, MySql
                SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}/{}'.format(
                    DB_ENGINE,
                    DB_USERNAME,
                    DB_PASS,
                    DB_HOST,
                    DB_NAME
                )

                USE_SQLITE = False

            except Exception as e:

                print('> Error: DBMS Exception: ' + str(e))
                print('> Fallback to SQLite ')
                
    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
            

    # Email server configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25) # 587
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # None
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # None
    ADMINS = ['brunex7900@gmail.com']