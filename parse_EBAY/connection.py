import sqlite3

sql = sqlite3.connect('ebay.db')

sql.execute(
    """
    CREATE TABLE ebay(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price TEXT,
        time TEXT,
        bids TEXT,
        link VARCHAR
    )
    """
)

sql.commit()
