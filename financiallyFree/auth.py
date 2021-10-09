import functools
from flask import(
    Blueprint, blueprints, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from financiallyFree.db import get_db

# ? Blueprint, to be able to route using /auth
auth = Blueprint('auth', __name__)

@auth.route('/register', methods = ('GET', 'POST'))
def register():
    checkErr = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = "Username cannot be left blank..."
        if not password:
            error = "Password cannot be left blank..."
        elif len(password) < 5:
            error = "Password must be greater than 5 characters..."
            
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
    return render_template("login.html")