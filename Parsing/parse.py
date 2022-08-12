from os import replace
import requests
from bs4 import BeautifulSoup
from requests.sessions import default_headers
import csv
import os

URL = 'https://auto.ria.com/uk/car/bmw/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36', 'accept':'*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'

def get_html (url, params=None):    #params - для того, чтобы спарсить все страницы на сайте
    r = requests.get(url, headers=HEADERS, params=params)
    return r 

def get_count_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_= 'page-item mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
    print (pagination)

def get_content (html):
    soup = BeautifulSoup(html, 'html.parser') # Создаются объекты Пайтон к которым мы можем обращатьсся и с которыми можем работать 
    items = soup.find_all('div', class_='content-bar' )  #Берет все секции страниц по URL

    cars = []
    for item in items:

        uah_price = item.find('span', class_ = 'i-block')
        if uah_price:
            uah_price = uah_price.get_text().replace('\xa0', ' ')
        else:
            print('Цену уточняйте')
        cars.append ({
            'title': item.find('div', class_ = 'item ticket-title').get_text(strip = True),#strip = True - чтобы обрезать концевые пробелы
            'link':  item.find('a', onclick = "_gaq.push(['_trackEvent', 'BuSearch', 'ClickOn_ad_photo', 'go_to_ad_page'])").get('href'),
            'usd_price': item.find('span', class_ = 'bold green size22', ).get_text(),
            'uah_price': uah_price ,
            'city': item.find('li', class_ = 'item-char view-location js-location').get_text().replace('( від )', '').replace('  ', '')
        }) # ВТОРОЕ НЕ МОГ НАЙТИ, НО В ИТОГЕ НАШЕЛ НА КАРТИНКЕ КАРТОЧКИ
    return cars 

def save_file (items, path):
    with open (path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter = ';' )   # file, delimiter = ';' - делит строки файла ;
        writer.writerow(['Марка', 'Сслыка', 'Цена в $', 'Цена  в UAH', 'Город'])

        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['uah_price'], item['city']])


def parse ():  # Основная функция 
    # URL = input('Введите свой URL: ')   # Вмест вверхней сссылки, передается ссылка, которую ввожит пользователь
    # URL = URL.strip()
    html = get_html(URL)
    if (html.status_code == 200) :  # html.status_code - возвращает измененую версию сервера прокси
        cars = []
        page_count = get_count_pages(html.text)
        for page in range (1, page_count + 1):
            print (f'Парсинг страницы {page} из {page_count}...')
            html = get_html (URL, params={'page': page})
            cars.extend(get_content(html.text))
        # save_file(cars, FILE)
        print(f'Получено {len(cars)} атвомобилей')
        os.startfile(FILE)
    else:
        print('Error')

parse()