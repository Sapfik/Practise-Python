import sqlite3

sql = sqlite3.connect('questions.sqlite')

sql.execute(
    """
    CREATE TABLE questions (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        link VARCHAR ,
        votes INTEGER,
        date DATETIME
    )
    """
)

sql.commit()