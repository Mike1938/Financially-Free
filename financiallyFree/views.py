from logging import error
import re
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

# ?This will query all the cattegories to be use as options for select tags
    catt = db.execute(
        "SELECT * FROM categories"
    ).fetchall()

# ? This will query and search in expenses the sum of all the expenses group by categories
    exCattData = db.execute(
        "SELECT categories.catName, sum(expenseAmount) AS 'exAmount' FROM expenses INNER JOIN categories ON categories.catID = expenses.catID WHERE expenses.userID = ?  GROUP BY catName" ,
        (g.user["userId"],)
    ).fetchall()

# ? This will query and get you the budget amount for each categories
    budgData = db.execute(
        "SELECT categories.catName, budgets.budgetAmount FROM budgets INNER JOIN categories ON categories.catID = budgets.catID WHERE userID = ?",
        (g.user["userId"],)
    ).fetchall()

    if request.method == "POST":
        if 'expenseSub' in request.form:
            title = request.form["expenseTitle"]
            exCatt = request.form["cattegory"]
            exAmount = float(request.form["expenseAmount"])
            expenseDate = request.form["exepenseDate"]
            didPay = request.form["didPay"]
            user = g.user["userId"]
            try:
                db.execute(
                    "INSERT INTO expenses(expenseName, expenseAmount, catID, userID, expenseDate, payed) VALUES (?,?,?,?,?,?)",
                    (title, exAmount, exCatt, user, expenseDate, didPay ),
                )
                db.commit()
            except db.IntegrityError:
                print("There was an error")
            else:
                return redirect(url_for("views.dashboard"))
        else:
            budgCatt = request.form["budCatt"]
            budgAmount = float(request.form["budgetAmount"])
            user = g.user["userId"]

            try:
                db.execute(
                    "INSERT INTO budgets(catID, budgetAmount, userID) VALUES (?,?,?)",
                    (budgCatt, budgAmount, user,)
                )
                db.commit()
            except db.IntegrityError:
                print("There Was a Problem")
            else:
                return redirect(url_for("views.dashboard"))
    db.close()
    return render_template("dashboard.html", catData = catt, exData = exCattData, budgetData = budgData)