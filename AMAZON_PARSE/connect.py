import sqlite3

sql = sqlite3.connect('videocards.sqlite')

sql.execute(
    """
    CREATE TABLE video_cards  (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        shorttitle TEXT,
        link VARCHAR,
        price BIGINT,
        reviews INTEGER
    )
    """
)

sql.commit()