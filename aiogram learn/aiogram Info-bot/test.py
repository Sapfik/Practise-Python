# url = 'https://hi-tech.news/other/3653-esche-odin-f-35-razbilsja-smotrite-na-novom-video.html'
# url = url.split('/')[-1].split('-')[0]
# print(url)

import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password ='ilya19072006',
    database = 'users'
)

mycursor = mydb.cursor()
# mycursor.execute("""CREATE TABLE users(id int PRIMARY KEY AUTO_INCREMENT, title TEXT, description TEXT, categorie TEXT, time DATETIME,article_id INTEGER, link VARCHAR)""")
# mydb.commit()

sql ='''CREATE TABLE IF NOT EXISTS users(
   id int PRIMARY KEY AUTO_INCREMENT,
   title TEXT,
   description TEXT,
   categorie TEXT,
   time TEXT,
   article_id INT,
   link VARCHAR(255)
)'''
mycursor.execute(sql)