DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS budgets;

CREATE TABLE users(
    userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    userName TEXT NOT NULL UNIQUE,
    userPass TEXT NOT NULL,
    fName TEXT NOT NULL,
    lName TEXT NOT NULL,
    dateReg TEXT NOT NULL
);

CREATE TABLE categories(
    catID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    catName TEXT NOT NULL
);

CREATE TABLE expenses(
    expenseID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    expenseName TEXT NOT NULL,
    expenseAmount REAL NOT NULL,
    catID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    expenseDate TEXT NOT NULL,
    payed TEXT NOT NULL DEFAULT "false",
    FOREIGN KEY(userID) REFERENCES users(userID),
    FOREIGN KEY(catID) REFERENCES categories(catID)
);

create TABLE budgets(
    budgetID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    catID TEXT NOT NULL,
    budgetAmount REAL NOT NULL,
    userID INTEGER NOT NULL,
    FOREIGN KEY(userID) REFERENCES users(userID),
    FOREIGN KEY(catID) REFERENCES categories(catID)
);

INSERT INTO categories(catName) VALUES
("Housing"), ("Transportation"), ("Food"),
("Utilities"), ("Insurance"), ("Car Payment"), ("Medical & Healthcare"),
("Personal Spending"), ("Recreation & Entertainment"), ("Miscellaneous"),
("Saving, Investing & Debt Payments");