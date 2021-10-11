from logging import error
from flask import Blueprint, render_template
from werkzeug.utils import redirect

from financiallyFree.auth import loginRequired

views = Blueprint('views', __name__)

@views.route('/')
def landingPage():
    return render_template('index.html')

@views.route('/dashboard')
@loginRequired
def dashboard():
    print("help")
    return render_template("dashboard.html")