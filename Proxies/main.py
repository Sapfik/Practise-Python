from os import terminal_size
import requests
from bs4 import BeautifulSoup
import re
from random import choice
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    'user-agent': ua.random,
    'accept' : '*/*'
}

# def main():
#     # URL = 'https://free.proxy-sale.com/'
#     # request = requests.get(url = URL, headers=headers)
#     # soup = BeautifulSoup(request.text, 'lxml')
    
#     for page in range(1, 20):
#         URL = f'https://free.proxy-sale.com/?proxy_page={page}'
#         request = requests.get(url = URL, headers=headers)
#         soup = BeautifulSoup(request.text, 'lxml')
#         ip = soup.find_all('td', class_ = 'ip')
#         for i in ip:
#             proxy = i.find('a').text.strip()
#             proxy = proxy.split('Нажмите')[0]
#             with open('proxy.txt', 'a', encoding='utf-8') as file:
#                 file.write(f'{proxy}\n')


def main2():
    # with open('http_proxies.txt', encoding='utf-8') as file:
    #     proxy_base = ''.join(file.readlines()).strip().split('\n')
    proxy_base = open('http_proxies.txt').readlines()    
    
        proxy = choice()
        proxies = {
            'http' : f'http://{proxy}'     
        }
        
        link = 'https://prom.ua'
        
        try:
            response = requests.get(link, proxies = proxies, timeout=10)
            print(f'IP: {response}')
            print(proxy)
            with open('third.txt', 'a', encoding='utf-8') as file:
                file.write(f'{proxy}\n')
        except:
            print('Не валидный')

main2()
# def main3():
#     URL = 'https://hidemy.name/ru/proxy-list/'
#     req = requests.get(url = URL, headers=headers)
#     soup = BeautifulSoup(req.text, 'lxml')
#     pagination = int(soup.find('div', class_ = 'pagination').find('ul').find_all('li')[-2].text)
    
#     for page in range(1, pagination+1):
#         url = f'https://hidemy.name/ru/proxy-list/?start={page*64}#list'
#         response = requests.get(url = url, headers=headers)
#         soup = BeautifulSoup(response.text, 'lxml')
        
#         proxies = soup.find('div', class_ = 'table_block').find('table').find_all('tr')
#         for proxy in proxies:
#             proxy = proxy.find('td').text.strip()
#             with open('next_level_proxy.txt', 'a', encoding='utf-8') as file:
#                 file.write(f'{proxy}\n')
        


# main()
        
    