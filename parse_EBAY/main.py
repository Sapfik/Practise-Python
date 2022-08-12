from itertools import product
from operator import index
import sqlite3
from wsgiref import headers
import requests 
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
import time
import pandas as pd

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'accept' : '*/*'
}
productList = []
searchitem = 'sony+ps5'
def get_data(searchitem):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={searchitem}&_sacat=0'
    req = requests.get(url = url, headers = headers)
    soup = BeautifulSoup(req.text, 'lxml')
    return soup

def parse(soup):
    sql = sqlite3.connect('ebay.db')
    cursor = sql.cursor()
    cards = soup.find_all('div', {'class' : 's-item__wrapper clearfix'})
    for card in cards:
        try:
            price = card.find('span', class_ = 's-item__price').text.strip()
        except:
            price  = None
        try:
            time = card.find('span', {'class' : 's-item__time s-item__time--soon'}).text.strip()
        except:
            time  = 'A lot of time'
            
        try:
            bids = card.find('span', class_ = 's-item__bids s-item__bidCount').text.strip()
        
        except:
            bids = 'Don`t have bids'
            
        product = {
        'title' : card.find('h3', class_ = 's-item__title').text.strip(),
        'soldprice' : price,
        'spend time' : time,
        'bids' : bids,
        'link' : card.find('a', class_ = 's-item__link')['href']
        }
        productList.append(product)
        
        cursor.execute(
            """
            INSERT INTO ebay (title, price, time, bids, link) VALUES (?, ?, ?, ?, ?)
            """, (card.find('h3', class_ = 's-item__title').text.strip(), price, time, bids,card.find('a', class_ = 's-item__link')['href'] )
        )
        
        sql.commit()
        
    return


def output(productList, searchitem):
    df = pd.DataFrame(productList)
    df.to_csv(f'{searchitem} ebay.csv', index = False)
    print('Saved')
    return

        
soup = get_data(searchitem=searchitem)
parse(soup)
output(productList, searchitem)
    