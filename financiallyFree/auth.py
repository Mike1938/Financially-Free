import functools
from os import error
import datetime
from flask import(
    Blueprint, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from financiallyFree.db import get_db

# ? Blueprint, to be able to route using /auth
auth = Blueprint('auth', __name__)
#  ? Function that verifies the user input
def verifyUsers(user, userPass,fName = None, lName = None):
    error = []
    if not user:
            error.append("Username cannot be left blank...")
    if not userPass:
            error.append("Password cannot be left blank...")
    elif len(userPass) < 5:
            error.append("Password must be greater than 5 characters...")
    if not fName == None or not lName == None:
        if not fName:
            error.append("First Name cannot be left blank...")
        if not lName:
            error.append("Last Name Cannot be left blank...")
    if error:
        return error
    else:
        return None

# ? This is going to register the user to the database, first is going to validate the info given by the users
# ? Then the database get initialize and the user data get inserted to the database if user already exist an alert will show if not it will be inserted and redirected to the login page

@auth.route('/register', methods = ('GET', 'POST'))
def register():
    if g.user:
        return redirect(url_for("views.dashboard"))
    checkErr = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fName = request.form['fName']
        lName = request.form['lName']
        regDate = datetime.datetime.now()
        db = get_db()
        error = verifyUsers(username, password, fName, lName)
            
        # ? Insert the user to the database
        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (userName, userPass, fName, lName, dateReg) VALUES (?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), fName, lName, regDate),
                )
                
                db.commit()
                
            except db.IntegrityError:
                error = f"The user {username} is already taken, please try again..."
            else: 
                return redirect(url_for("auth.login"))

        checkErr = error
    return render_template('register.html', err = checkErr)

# ? Log in user route, this is going to check the form of the user and find them in the database if not an error will be show to the user
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

# ? This is going to check before every request request if the user is logged in and search the database for the information
@auth.before_app_request
def load_User():
    userId = session.get('userId')
    if userId is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM users WHERE userId = ?", (userId,)
        ).fetchone()

# ?Verifies that the user is logged in when accesing request
def loginRequired(view):
    @functools.wraps(view)
    def wrappedView(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrappedView

# ? Logout user and clear the session cookies
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.landingPage'))