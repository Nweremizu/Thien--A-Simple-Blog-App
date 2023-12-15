from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404_error.html')


@app.errorhandler(500)
def internal_error(error):
    return render_template('error/500_error.html')
