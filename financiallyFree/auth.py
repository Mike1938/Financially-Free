import functools
from os import error
from flask import(
    Blueprint, blueprints, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from financiallyFree.db import get_db

# ? Blueprint, to be able to route using /auth
auth = Blueprint('auth', __name__)
def verifyUsers(user, userPass):
    error = []
    if not user:
            error.append("Username cannot be left blank...")
    if not userPass:
            error.append("Password cannot be left blank...")
    elif len(userPass) < 5:
            error.append("Password must be greater than 5 characters...")
    if error:
        return error
    else:
        return None

@auth.route('/register', methods = ('GET', 'POST'))
def register():
    checkErr = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = verifyUsers(username, password)
            
        # ? Insert the user to the database
        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (userName, userPass) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                
                db.commit()
                
            except db.IntegrityError:
                error = f"The user {username} is already taken, please try again..."
            else: 
                return redirect(url_for("auth.login"))

        checkErr = error
    return render_template('register.html', err = checkErr)

@auth.route('/login', methods=('GET', 'POST'))
def login():
    checkErr = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = verifyUsers(username, password)
        if error is None:
            user = db.execute(
                "SELECT * FROM users WHERE userName = ?", (username,)
            ).fetchone()

            if user is None:
                error = ["User could not be found"]
            elif not check_password_hash(user['userPass'], password):
                error = ["password is incorrect please try again"]
            if error is None:
                session.clear()
                session['userId'] = user['userID']
                return redirect(url_for('views.dashboard'))
        checkErr = error
    return render_template("login.html", err = checkErr)

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.landingPage'))