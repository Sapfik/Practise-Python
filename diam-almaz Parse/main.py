from lib2to3.pgen2 import driver
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
async def get_categories_links(session):
    url = 'https://diam-almaz.ru/'
    async with session.get(url = url, headers = headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        links = soup.find_all('a' ,class_ = 'ui-home-category__name')
        for link in links:
            link = 'https://diam-almaz.ru'+link['href']

            
            
async def get_data(session, url):
    pass  
        
async def get_second_links(file_path):
    tasks =[]
    async with aiohttp.ClientSession() as session:
        with open(file_path, encoding='utf-8') as file:
            urls = [line.strip() for line in file.readlines()]

        for url in urls:
            response = await session.get(url = url, headers = headers)
            soup = BeautifulSoup(await response.text(), 'lxml')
            cards = soup.find_all('a', class_ = 'ce__info-block_title vendor-category-title')
            for card in cards:
                card = card['href']
                print(card)
        #         task_new = asyncio.create_task(get_data(session=session, url = card))
        #         tasks.append(task_new)
                
        # await asyncio.gather(*tasks)
                

        
        
def main():
    # get_categories_links(url = 'https://diam-almaz.ru/')
    asyncio.run(get_second_links(file_path = r'D:\Practise Python\Practise_parsing\diam-almaz Parse\first_links.txt'))
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    finish_time = time.time() - start_time
    print(f'Потрачено: {finish_time}')
    
    
if __name__ == '__main__':
    main()