from os import replace
import requests
from bs4 import BeautifulSoup
#from requests.sessions import default_headers
import csv
import os

URL = 'https://freelance.ua/orders/'
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36', 'accept': '*/*'}

def get_html (url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content (html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all ('li', class_= 'j-order')
    cards = []
    for item in items:
        cards.append ({
            'title': item.find('header', class_= 'l-project-title').get_text(strip = True),
            'link': item.find ('header', class_= 'l-project-title').find_next('a').get('href'),
            'uah_price': item.find('span', class_= 'l-price').get_text(), 
            'main_text': item.find('div', class_ = 'l-project-head flex-price-tag').find_next('article').find_next('p').get_text(),
            'city': item.find ('ul', class_= 'l-item-features').replace('\r\n\r\n', '').get_text()
        })
    print (cards)

def parse ():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)

    else:
        print ("Что-то пошло не по плану =(")

parse()

