import requests
from bs4 import BeautifulSoup
import csv
import re
import time 
import asyncio
import aiohttp
from fake_useragent import UserAgent

class Parser:
    def __init__(self):
        self.categoty_list = []
        self.page_links = []
        self.drink_links = []
        self.csv_rows = []
        self.csv_name = 'test.csv'
        self.basic_url = 'https://simplewine.ru'
        self.ua = UserAgent()
        self.headers = {
            'accept' : '*/*',
            'user-agent' : self.ua.random
        }
        
    def parse_categories(self):
        response = requests.get(url = self.basic_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        row_categories = soup.find('ul', class_ = 'navigation__list container').find_all('li', class_ = 'navigation__item')
        for index in [0,1,4]:
            link = self.basic_url + row_categories[index].find('a', class_ = 'navigation__link').get('href')
            #row_categories[index] - выбираем каждый li по индексу (который нам нужен)
            self.categoty_list.append(link)
        
        
    def create_page_links(self):
        self.pages_pc = []
        
        for link in self.categoty_list:
            numbers = []
            req = requests.get(url = link, headers=self.headers)
            soup = BeautifulSoup(req.text, 'lxml')
            pagination = int(soup.find('div', class_ = 'pagination__navigation').find_all('a')[-2].text.strip())
            
            self.pages_pc.append(pagination)
            
        for last_page, link in zip(self.pages_pc, self.categoty_list):
            self.page_links.append(link)
            for i in range(1, last_page + 1):
                page_link = f'{link}page{i}/'
                self.page_links.append(page_link)
                
        print(self.page_links)
            
        
                   
    def main(self):
        self.parse_categories()
        self.create_page_links()
        
if __name__ == '__main__':
    parser = Parser()
    parser.main()
        
        