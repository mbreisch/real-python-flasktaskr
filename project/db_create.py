import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

    c=connection.cursor()

    # CREATE TABLE
    c.execute("""CREATE TABLE IF NOT EXISTS tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
                  due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL )""")

    # INSERT dummy data
    c.execute("INSERT INTO tasks(name,due_date,priority,status) VALUES('Finish this tutorial','01/20/2016',10,1)")
    c.execute("INSERT INTO tasks(name,due_date,priority,status) VALUES('Eat lunch','01/19/2016',10,1)")
