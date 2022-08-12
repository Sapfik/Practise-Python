from aiohttp import ClientSSLError
from aiosqlite import Cursor
import requests
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime
import timestring
import mysql.connector

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'accept' : '*/*'
}

def get_articles():
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'ilya19072006',
        database = 'users'
    )
    
    mycursor = mydb.cursor()
    articles = {}
    url = 'https://hi-tech.news/'
    
    req = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    cards = soup.find_all('div' , {'class' : 'post-body'})
    for card in cards:
        title = card.find('a', class_ = 'post-title-a').text.strip()
        link = card.find('a', class_ = 'post-title-a')['href']
        id = link.split('/')[-1].split('-')[0]
        description = card.find('div', class_ = 'the-excerpt').text.strip()
        categorie = card.find('div', class_ = 'post-media-category').text.strip()
        time = card.find('div', class_ = 'post-detail pd-padding').find('a').text.replace(';', ':').strip()
        # datetime_object = datetime.strptime(time, '%d-%b, %I;%M')
        datetime = timestring.Date(time).date    #Переделываем время в более читабельный вид

        mycursor.execute('''CREATE TABLE IF NOT EXISTS users(
           id int PRIMARY KEY AUTO_INCREMENT,
           title TEXT,
           description TEXT,
           categorie TEXT,
           time TEXT,
           article_id INT,
           link VARCHAR(255)
        )''')     #VARCHAR - всегда указывается с колиством символов, которые он будет содержать
        mycursor.execute('SELECT description FROM users WHERE description = %s', (description, ))
        data = mycursor.fetchall()
        if not data:
            mycursor.execute("INSERT INTO users (title, description, categorie, time, article_id, link) VALUES (%s, %s, %s , %s, %s, %s)", (title, description, categorie, time, id, link))
            mydb.commit()
            articles[id] = {
                'Title': f"✏️  {title}",
                'Link': f"{link}",
                'Description': f"📌 {description}",
                'Categorie': f"⚠️  {categorie}",
                'Datetime': f"🕒 {datetime}"
            }
        else:
            pass

    return articles

