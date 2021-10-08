

CREATE TABLE users(
    userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    userName TEXT NOT NULL,
    passWord TEXT NOT NULL,
    dateCreated TEXT NOT NULL
);

CREATE TABLE cattegories(
    cattID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    cattName TEXT NOT NULL
);

CREATE TABLE expenses(
    expenseID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    expenseName TEXT NOT NULL,
    expenseAmount REAL NOT NULL,
    cattID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    expenseDate TEXT NOT NULL,
    payed TEXT NOT NULL DEFAULT "false",
    FOREIGN KEY(userID) REFERENCES users(userID),
    FOREIGN KEY(cattID) REFERENCES cattegories(cattID)
);

create TABLE savings(
    savingID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    savingName TEXT NOT NULL,
    savingAmount REAL NOT NULL,
    savingDate TEXT NOT NULL,
    cattID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    FOREIGN KEY(cattID) REFERENCES cattegories(cattID),
    FOREIGN KEY(userID) REFERENCES users(userID)
);