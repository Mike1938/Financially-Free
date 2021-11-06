import datetime
from logging import error
from os import close
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
    months = {}
    db = get_db()
    date = f"{datetime.datetime.now().year}-{datetime.datetime.now().month}"
    readableDate = f"{datetime.datetime.now().strftime('%B')} - {datetime.datetime.now().year}" 
    # *Check if the user used the select month expenses(data in url)
    if request.args.get("yearMonth"):
        searchDate = request.args.get("yearMonth")
    else:
        searchDate = date
    # * Function that turn month numbers to readable strings
    def readableMonth(data):
        dashLocation = data.find("-")
        year = data[:dashLocation]
        readableDate = data[dashLocation + 1:]
        if readableDate == "01":
            return f"{year} - January"
        elif readableDate == "02":
            return f"{year} - February"
        elif readableDate == "03":
            return f"{year} - March"
        elif readableDate == "04":
            return f"{year} - April"
        elif readableDate == "05":
            return f"{year} - May"
        elif readableDate == "06":
            return f"{year} - June"
        elif readableDate == "07":
            return f"{year} - July"
        elif readableDate == "08":
            return f"{year} - August"
        elif readableDate == "09":
            return f"{year} - September"
        elif readableDate == "10":
            return f"{year} - October"
        elif readableDate == "11":
            return f"{year} - November"
        elif readableDate == "12":
            return f"{year} - December"
    
    readMonthYear =readableMonth(searchDate)

    # ?This will query all the cattegories to be use as options for select tags
    catt = db.execute(
        "SELECT * FROM categories"
    ).fetchall()

    # ? This will query and search in expenses the sum of all the expenses group by categories
    exCattData = db.execute(
        "SELECT categories.catName, sum(expenseAmount) AS 'exAmount', SUBSTR(expenseDate, 1, 7) AS dateInfo, expenseDate FROM expenses INNER JOIN categories ON categories.catID = expenses.catID WHERE expenses.userID = ? AND dateInfo = ?  GROUP BY catName" ,
        (g.user["userId"], searchDate,)
    ).fetchall()

    # ? This will query the DB and group by month and year and sum all the expenses of the month
    monthlyEx = db.execute(
         "SELECT SUBSTR(expenseDate, 1, 7) AS dateInfo, SUM(expenseAmount) AS sumTotal, expenseID FROM expenses INNER JOIN categories ON categories.catID = expenses.catID WHERE expenses.userID = ? GROUP BY dateInfo",
         (g.user["userId"],)
    ).fetchall()
    
    # ? Looping to append the month and year, to be use for check expenses month form
    for d in monthlyEx:
        months[readableMonth(d["dateInfo"])] = d["dateInfo"]

    # ? This will query all the transactions of the month
    allExpenses = db.execute(
        "SELECT expenseName, categories.catName, printf('%.2f',expenseAmount) as exAmount, expenseDate, SUBSTR(expenseDate, 1,7) AS monthYear, expenseID FROM expenses INNER JOIN categories ON categories.catID = expenses.catID WHERE expenses.userID = ? AND monthYear = ? ORDER BY expenseDate DESC",
        (g.user["userId"], searchDate,)
    ).fetchall()

    # ? This will query and get you the budget amount for each categories
    # budgData = db.execute(
    #     "SELECT categories.catName, budgets.budgetAmount, sum(expenses.expenseAmount) as sumAmount, SUBSTR(expenses.expenseDate, 1, 7) AS dateInfo, monthYear FROM budgets INNER JOIN categories ON categories.catID = budgets.catID INNER JOIN expenses on expenses.catID = categories.catID WHERE budgets.userID = ? AND dateInfo = ? AND monthYear = ? GROUP BY categories.catID",
    #     (g.user["userId"], searchDate, searchDate,)
    # ).fetchall()

    budgetInfo = db.execute(
        "SELECT categories.catName, budgets.budgetAmount FROM budgets INNER JOIN categories ON categories.catID = budgets.catID WHERE userID = ? AND monthYear = ? ORDER BY categories.catID",
        (g.user["userId"], searchDate,)
    ).fetchall()

    expenseSum = db.execute(
        "SELECT categories.catName, sum(expenseAmount) AS expenseSum, SUBSTR(expenses.expenseDate, 1, 7) AS dateInfo FROM expenses INNER JOIN categories ON categories.catID = expenses.catID WHERE userID = ? AND dateInfo = ? GROUP BY categories.catID ORDER BY categories.catID",
        (g.user["userId"], searchDate,)
    ).fetchall()
    budgeteLen = len(budgetInfo)
    budgetExpen = []
    for num in range(0, budgeteLen):
        budgetExpen.append({
            "category": budgetInfo[num]["catName"],
            "budgetAmount": budgetInfo[num]["budgetAmount"],
            "expenseAmount": expenseSum[num]["expenseSum"]
        })
        print(budgetExpen)

    # ? function to strip string whitespaces
    def stripInputs(data):
        return data.strip()

    # ?Function to check if the values are not empty return none if no errors
    def checkInputs(valuesObj):
        errors = []
        for key, val in valuesObj.items():
            if not val:
                errors.append(f"{key} was left empty...")
        if errors:
            return errors
        else:
            return None

    checkingEx = None
    checkingBudg = None

    # ? Post section of the dasboard
    if request.method == "POST":
        if 'expenseSub' in request.form:
            title = stripInputs(request.form["expenseTitle"])
            exCatt = request.form["cattegory"]
            try:
                exAmount = float(request.form["expenseAmount"])
                exAmount = format(exAmount, ".2f")
            except:
                exAmount= ""
            
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
                    return redirect(request.url)
        if 'budgetButt' in request.form:
            budgCatt = request.form["budCatt"]
            try:
                budgAmount = float(request.form["budgetAmount"])
                budgAmount = format(budgAmount, ".2f")
            except:
                budgAmount = ""
        
            budgMonth = request.form["month"]
            budgYear = str(request.form["year"])

            user = g.user["userId"]

            inputVals = {
                "Budget Amount": budgAmount,
                "Budget Month": budgMonth,
                "Budget Year": budgYear
            }
            monthYear = f"{budgYear}-{budgMonth}"
            checkingBudg = checkInputs(inputVals)
            if checkingBudg is None:

                # * This check if the budget has already been set
                checkBudg = db.execute(
                "SELECT budgetID FROM budgets WHERE userID = ? AND catID = ? AND monthYear = ?",
                (user, budgCatt, monthYear,)
                ).fetchone()
                if  checkBudg:
                    # *This is updating the set budget to the new amount
                    db.execute(
                        "UPDATE budgets SET budgetAmount = ? WHERE budgetID =?",
                        (budgAmount, checkBudg["budgetID"],)
                    )
                    db.commit()
                else:
                    try:
                        db.execute(
                            "INSERT INTO budgets(catID, budgetAmount, monthYear, userID) VALUES (?,?,?,?)",
                            (budgCatt, budgAmount, monthYear, g.user["userId"],)
                        )
                        db.commit()
                    except db.IntegrityError:
                        print("There Was a Problem")
                    else:
                        return redirect(request.url)
        # * This is the delete expense section
        if 'deleteExpense' in request.form:
            expenseId = request.form["deleteExpense"]
            try:
                db.execute(
                    "DELETE FROM expenses WHERE expenseID = ?",
                    (expenseId,)
                )
                db.commit()
            except:
                print("There was a problem")
            else:
                return redirect(request.url)
        db.close()
    return render_template("dashboard.html", catData = catt, exData = exCattData, budgetData = budgetInfo, expenseD = expenseSum, dataDate = {"fullDate": date, "readDate": readMonthYear, "monthYear": months}, monthGEx = monthlyEx, check = checkingEx, checkBud = checkingBudg, allExpense = allExpenses)