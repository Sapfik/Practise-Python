from asyncio import sleep
from lib2to3.pgen2 import driver
from urllib.parse import ParseResultBytes
from requests_html import HTMLSession    #Библиотека, которая работает через запросы и сесиии (имеет такжу функцию асинхроного парсинга)
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Объект Session позволяет сохранять определенные параметры между запросами. Он же сохраняет куки всех запросов, сделанных из экземпляра Session.
#Поэтому, если делать несколько запросов к одному и тому же хосту, базовое TCP-соединение будет использоваться повторно, что приводит к значительному увеличению производительности.


s = HTMLSession()    #Создаем сессию

url = 'https://www.amazon.com/s?k=videocards&crid=3OLZE764CLM94&sprefix=videocards%2Caps%2C236&ref=nb_sb_noss'

def getdata(url):    #Эта функция позволяет нам получить полный html файл по ссылке, для того, чтобы мы могли дальше спокойно работать
    r = s.get(url)
    r.html.render()      #Отоброзит весь javascript и поэттому не будем заблокированны Амазоном (точечный рендеринг, чтобы Амазон не говорил, что это 'Бот')
    soup = BeautifulSoup(r.html.html, 'html.parser')    #Пытаемся отдать супу наш отрендеренный html code   
    
    return soup



def getdeals(soup):
    products = soup.find_all('div', {'data-component-type' : 's-search-result'})   #Находим все товары
    for item in products:
        title = item.find('a', {'class' : 'a-link-normal'}).text.strip()
        short_title = item.find('a', {'class' : 'a-link-normal'}).text.strip()[:25]    #Делаем более короткий текст для того, чтобы у нас не было супер огромного текста на всю страницу
        link = item.find('a', {'class' : 'a-link-normal'})['href']
        print(f'{short_title} | {link}')
        
print(getdata(url = url))

