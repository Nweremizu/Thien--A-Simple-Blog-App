from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor, CKEditorField
from flask_moment import Moment

app = Flask(__name__)

# load config from config.py
app.config.from_object(Config)

# Initialize the Flask extensions
db = SQLAlchemy(app)  # database instance
migrate = Migrate(app, db)  # database migration engine
login = LoginManager(app)  # login manager
login.login_view = 'login'  # login view function
ckeditor = CKEditor(app)  # rich text editor
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_PKG_TYPE'] = 'full'
moment = Moment(app)  # time and date formatting

from app import routes, models, errors
