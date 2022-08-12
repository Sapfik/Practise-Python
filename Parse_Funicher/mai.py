from asyncio import sleep
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession, HTML
from fake_useragent import UserAgent
from selenium import webdriver
import cloudscraper
import time
import os


ua = UserAgent()
headers = {
    'user-agent' : ua.random,
    'accept' : '*/*'
}

def get_first_links(url):
    # req = requests.get(url = url, headers=headers)
    # print (req.text)
    
    # scraper = cloudscraper.create_scraper()
    # print(scraper.get(url = url, headers=headers).text)
    
    # s = HTMLSession()
    # r = s.get(url = url, headers=headers)
    # r.html.render(sleep = 10000)
    # soup = BeautifulSoup(r.html.html, 'html.parser')
    
    # all_categories = soup.find_all('li', {'class' : 'header-nav__category header-nav__category_1'})
    # for categorie in all_categories:
    #     categorie = categorie.find('a')['href']
    
    driver = webdriver.Chrome(executable_path=r'D:\Practise Python\Parse_Funicher\chromedriver.exe')
    driver.get(url)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    all_categories = soup.find_all('li', {'class' : 'header-nav__category header-nav__category_1'})
    for categorie in all_categories:
        categorie = 'https://pm.ru/' + categorie.find('a')['href']
        with open('first_links.txt', 'a', encoding='utf-8') as file:
            file.write(f'{categorie}\n')
        
def get_all_links(file_path):
    with open(file_path, encoding='utf-8') as file:
        urls = [line.strip() for line in file.readlines()]
        
    for url in urls:
        # s = HTMLSession()
        # r = s.get(url = url, headers=headers)
        # r.html.render(sleep = 2)
        # soup = BeautifulSoup(r.html.html, 'html.parser')
        # print(r.html.html)
        
        # req = requests.get(url = url, headers=headers)
        # soup = BeautifulSoup(req.text, 'lxml')
        # print(req.text)
        
        driver = webdriver.Chrome(executable_path=r'D:\Practise Python\Parse_Funicher\chromedriver.exe')
        driver.get(url)
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        all_links = soup.find_all('li', class_ = 'filter-secondary__col')
        for link in all_links:
            link = 'https://pm.ru/' + link.find('a')['href']
            with open('links.txt', 'a', encoding='utf-8') as file:
                file.write(f'{link}\n')
            
        driver.close()
        driver.quit()
            

def getdata(file_path):
    sofas = []
    with open(file_path, encoding='utf-8') as file:
        urls = [line.strip() for line in file.readlines()]
    
    count = 1
    for url in urls[:1]:
        # s = HTMLSession()
        # r = s.get(url = url, headers=headers)
        # r.html.render(sleep = 20)
        # soup = BeautifulSoup(r.html.html, 'html.parser')
        # print(r.html.html)
        
        # driver = webdriver.Chrome(executable_path=r'D:\Practise Python\Parse_Funicher\chromedriver.exe')
        # driver.get(url)
        # driver.implicitly_wait(10)
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(driver.page_source)
        with open('index.html', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        
        main_id = soup.find('div', class_ = 'page-title-sorting and-count').find('span', class_ = 'counter').text.strip()

        cards = soup.find_all('div', class_ = 'good__link-wrapper')
        for card in cards[:5]:
            link = 'https://pm.ru' + card.find('a' ,class_ = 'good__link')['href']
            
            # s = HTMLSession()
            # r = s.get(url = 'https://pm.ru', headers = headers)
            # js = s.get(url = link, headers = headers).text
            
            # r.html.render()
            # r.html.render(script = js)
            # print(r.html.html)
            

            driver = webdriver.Chrome(executable_path=r'D:\Practise Python\Parse_Funicher\chromedriver.exe')
            driver.get(link)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            driver.close()
            driver.quit()
            
            title = soup.find('h1', class_ = 'catalog-header__title').text.strip()
            price = soup.find('span', {'class' : 'price_no_rub'}).text.strip()
            character = soup.find('div', class_ = 'dimensions_block').text.replace('                ', '').strip()
            articul = soup.find('div', class_ = 'catalog-header__info').find('span').text.strip()
            image = 'https://pm.ru' + soup.find('a', class_ = 'js-open-preview').find('img')['srcset']

            r = requests.get(url = image, headers=headers)
            with open(f'data/{articul}.jpg', 'wb') as file:
                file.write(r.content)
                
            data = {
                'title' : title,
                'price' : price,
                'character' : character,
                'articul' : articul,
                'categorie id' : main_id  
            }
            
            sofas.append(data)
            
        
            
    df = pd.DataFrame(sofas)
    df.to_excel('sofas.xlsx', index=False)

def main():
    # get_first_links(url = 'https://pm.ru/')
    # get_all_links(file_path=r'D:\Practise Python\Parse_Funicher\first_links.txt')
    getdata(file_path=r'D:\Practise Python\Parse_Funicher\links.txt')
    
if __name__ == '__main__':
    main()
