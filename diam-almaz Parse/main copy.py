from lib2to3.pgen2 import driver
from cv2 import line
import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
from fake_useragent import UserAgent
from selenium import webdriver
import time
import asyncio
import aiohttp
import datetime

ua = UserAgent()

headers = {
    'user-agent' : ua.random,
    'accept' : '*/*'
}

urls = []
start_time = time.time()
def get_categories_links(url):
    req = requests.get(url = url, headers = headers)
    soup = BeautifulSoup(req.text, 'lxml')
    links = soup.find_all('a' ,class_ = 'ui-home-category__name')
    for link in links:
        link = 'https://diam-almaz.ru'+link['href']
        with open('first_links.txt', 'a', encoding='utf-8') as file:
            file.write(f'{link}\n')
        
                
def get_second_links():
    with open('first_links.txt', encoding = 'utf-8') as file:
        urls = [line.strip() for line in file.readlines()]
        
    print(urls)
        
        
def main():
    get_categories_links(url = 'https://diam-almaz.ru/')
    get_second_links()
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    finish_time = time.time() - start_time
    print(f'Потрачено: {finish_time}')
    
    
if __name__ == '__main__':
    main()