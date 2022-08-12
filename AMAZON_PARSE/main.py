from asyncio import sleep
from lib2to3.pgen2 import driver
from urllib.parse import ParseResultBytes
from requests_html import HTMLSession    #Библиотека, которая работает через запросы и сесиии (имеет такжу функцию асинхроного парсинга)
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import sqlite3

from sqlalchemy import sql

# Объект Session позволяет сохранять определенные параметры между запросами. Он же сохраняет куки всех запросов, сделанных из экземпляра Session.
#Поэтому, если делать несколько запросов к одному и тому же хосту, базовое TCP-соединение будет использоваться повторно, что приводит к значительному увеличению производительности.


s = HTMLSession()    #Создаем сессию
dealList = []
url = 'https://www.amazon.com/s?k=videocards&crid=3OLZE764CLM94&sprefix=videocards%2Caps%2C236&ref=nb_sb_noss'

def getdata(url):    #Эта функция позволяет нам получить полный html файл по ссылке, для того, чтобы мы могли дальше спокойно работать
    driver = webdriver.Chrome(executable_path= r'D:\Practise Python\Practise_parsing\AMAZON_PARSE\chromedriver.exe')
    driver.get(url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')    #Пытаемся отдать супу наш отрендеренный html code   
    driver.close()
    driver.quit()
    return soup



def getdeals(soup):
    sql = sqlite3.connect('videocards.sqlite')
    cursor = sql.cursor()
    products = soup.find_all('div', {'data-component-type' : 's-search-result'})   #Находим все товары
    for item in products:
        title = item.find('h2', class_ = 'a-size-mini').text.strip()
        short_title = item.find('h2', class_ = 'a-size-mini').text.strip()[:25]    #Делаем более короткий текст для того, чтобы у нас не было супер огромного текста на всю страницу
        link = 'https://www.amazon.com' + item.find('a', {'class' : 'a-link-normal'})['href']
        try:
            price = item.find('span', class_ = 'a-offscreen').text.replace('$', '').strip()
        except:
            price = None
        
        try:
            reviews = item.find('span', class_ = 'a-size-base').text.strip()
        except:
            reviews = 0  
            
        card = {
            'title' : title,
            'short-title' : short_title,
            'link' : link,
            'price' : price,
            'reviews' : reviews
        }
        cursor.execute(
            """
            INSERT INTO video_cards (title, shorttitle, link, price, reviews) VALUES (?, ?, ?, ?, ?)
            """, (title, short_title, link, price, reviews)
        )
        sql.commit()
        dealList.append(card)

    return

def getnextpage(soup):
    pages = soup.find('span', class_ = 's-pagination-strip')
    if not pages.find('li', class_ = 's-pagination-disabled'):     #Если не находит отключенную кноку 'NEXT', то тогда мы находим эту кнопку и берем от нее ссылку к следующей странице
        url = 'https://www.amazon.com' + pages.find_all('a', class_ = 's-pagination-separator')[-1]['href']
        return url
    else:
        return
        

sql = sqlite3.connect('videocards.sqlite')
cursor = sql.cursor()        
while True:
    soup = getdata(url = url)    #url - тот, который ниже
    getdeals(soup)  
    url = getnextpage(soup)   
    if not url:   # Если нету ссылки на следующию страницу, то мы просто выходим из цикла
        break
    else:    # Если есть, то выводим
        print(url)
        print(len(dealList))
        

df = pd.read_sql_query('SELECT * FROM videocards', sql)
print(df)
sql.close()