import sqlite3

sql = sqlite3.connect('countries.sqlite')

sql.execute(
    """
    CREATE TABLE countries(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        russion_text TEXT,
        english_text TEXT,
        symbols_text TEXT
    )
    """
)

sql.commit()