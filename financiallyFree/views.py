from logging import error
from flask import Blueprint, render_template
from werkzeug.utils import redirect

views = Blueprint('views', __name__)

@views.route('/')
def landingPage():
    return render_template('index.html')

@views.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")