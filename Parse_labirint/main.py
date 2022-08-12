from operator import ne
from urllib import request
import requests
from bs4 import BeautifulSoup
from random import choice
from lxml import html
from selenium import webdriver
import time
from requests.auth import HTTPProxyAuth

with open('proxy_list.txt', encoding='utf-8') as file:
    proxy_list = ''.join(file.readlines()).strip().split('\n')
    
headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'accept' : '*/*'
}
def get_data(url):
    s = requests.Session()
    
    proxy = choice(proxy_list)
    proxies = {
        'http' : f'http://{proxy}',
        'https' : f'https://{choice(proxy_list)}'
    }
    
    # Проблема прокси не в авторизации
    auth = HTTPProxyAuth("gRRT7n", "NMu8g0")
    s.auth = auth
    response = s.get(url = url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    driver = webdriver.Chrome(executable_path=r'D:\Practise Python\Practise_parsing\Parse_labirint\chromedriver.exe')
    driver.get(url)
    # tree = html.fromstring(response.content)     #Один из вариантов поиска по xpath
    time.sleep(10)
    print(response.text)
    pagination = int(soup.find('div',class_ = 'pagination-numbers').find_all('a')[-1].text)

    print(pagination)

def main():
    get_data(url = 'https://www.labirint.ru/genres/2308/?display=table')
    
if __name__ == '__main__':
    main()