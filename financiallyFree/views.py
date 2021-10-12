from logging import error
from flask import Blueprint, render_template , request , g
from flask.helpers import url_for
from werkzeug.utils import redirect
from financiallyFree.auth import get_db
from financiallyFree.auth import loginRequired


views = Blueprint('views', __name__)

@views.route('/')
def landingPage():
    return render_template('index.html')

@views.route('/dashboard', methods= ("GET", "POST"))
@loginRequired
def dashboard():
    db = get_db()
    catt = db.execute(
        "SELECT * FROM cattegories"
    ).fetchall()
    exCattData = db.execute(
        "SELECT cattegories.cattName, sum(expenseAmount) FROM expenses INNER JOIN cattegories ON cattegories.cattID = expenses.cattID GROUP BY cattName"
    ).fetchall()
    
    if request.method == "POST":
        title = request.form["expenseTitle"]
        exCatt = request.form["cattegory"]
        exAmount = int(request.form["expenseAmount"])
        expenseDate = request.form["exepenseDate"]
        didPay = request.form["didPay"]
        user = g.user["userId"]
        try:
            db.execute(
                "INSERT INTO expenses(expenseName, expenseAmount, cattID, userID, expenseDate, payed) VALUES (?,?,?,?,?,?)",
                (title, exAmount, exCatt, user, expenseDate, didPay ),
            )
            db.commit()
        except db.IntegrityError:
            print("There was an error")
        else:
            print("It was subbmited")
            return redirect(url_for("views.dashboard"))
    return render_template("dashboard.html", cattData = catt)