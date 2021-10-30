import datetime
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
    date = f"{datetime.datetime.now().year}-{datetime.datetime.now().month}"
    readableDate = f"{datetime.datetime.now().strftime('%B')} - {datetime.datetime.now().year}" 
    # ?This will query all the cattegories to be use as options for select tags
    catt = db.execute(
        "SELECT * FROM categories"
    ).fetchall()

    # ? This will query and search in expenses the sum of all the expenses group by categories
    exCattData = db.execute(
        "SELECT categories.catName, sum(expenseAmount) AS 'exAmount', SUBSTR(expenseDate, 1, 7) AS dateInfo, expenseDate FROM expenses INNER JOIN categories ON categories.catID = expenses.catID WHERE expenses.userID = ? AND dateInfo = ?  GROUP BY catName" ,
        (g.user["userId"], date,)
    ).fetchall()

    # ? This will query the DB and group by month and year and sum all the expenses of the month
    monthlyEx = db.execute(
         "SELECT SUBSTR(expenseDate, 1, 7) AS dateInfo, SUM(expenseAmount) AS sumTotal FROM expenses INNER JOIN categories ON categories.catID = expenses.catID WHERE expenses.userID = ? GROUP BY dateInfo",
         (g.user["userId"],)
    ).fetchall()

    # ? This will query and get you the budget amount for each categories
    budgData = db.execute(
        "SELECT categories.catName, budgets.budgetAmount, sum(expenses.expenseAmount) as sumAmount, SUBSTR(expenses.expenseDate, 1, 7) AS dateInfo FROM budgets INNER JOIN categories ON categories.catID = budgets.catID INNER JOIN expenses on expenses.catID = categories.catID WHERE budgets.userID = ? AND dateInfo = ? GROUP BY categories.catID",
        (g.user["userId"], date,)
    ).fetchall()
    def checkInputs(valuesObj):
        errors = []
        for key, val in valuesObj.items():
            if not val:
                errors.append(f"{key} was left empty...")
        print(errors)
        if errors:
            return errors
        else:
            return None
    checkingEx = None
    checkingBudg = None
    if request.method == "POST":
        if 'expenseSub' in request.form:
            title = request.form["expenseTitle"]
            exCatt = request.form["cattegory"]
            try:
                exAmount = float(request.form["expenseAmount"])
                exAmount = "{:.2f}".format(exAmount)
            except:
                exAmount = ""
            expenseDate = request.form["exepenseDate"]
            user = g.user["userId"]
            inputVals = {
                "Title": title,
                "Expense Category": exCatt,
                "Expense Amount": exAmount,
                "Expense Date": expenseDate,
                "User": user
            }
            checkingEx = checkInputs(inputVals)

            if checkingEx is None:
                try:
                    db.execute(
                        "INSERT INTO expenses(expenseName, expenseAmount, catID, userID, expenseDate) VALUES (?,?,?,?,?)",
                        (title, exAmount, exCatt, user, expenseDate),
                    )
                    db.commit()
                except db.IntegrityError:
                    print("There was an error")
                else:
                    return redirect(url_for("views.dashboard"))
        if 'budgetButt' in request.form:
            budgCatt = request.form["budCatt"]
            try:
                budgAmount = float(request.form["budgetAmount"])
                budgAmount = "{:.2f}".format(budgAmount)
            except:
                budgAmount = ""
            user = g.user["userId"]
            inputVals = {
                "Budget Amount": budgAmount
            }
            checkingBudg = checkInputs(inputVals)
            if checkingBudg is None:
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
    return render_template("dashboard.html", catData = catt, exData = exCattData, budgetData = budgData, dataDate = {"fullDate": date, "readDate": readableDate}, monthGEx = monthlyEx, check = checkingEx, checkBud = checkingBudg)