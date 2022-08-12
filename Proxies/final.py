import requests
from bs4 import BeautifulSoup
import csv
import pandas
import time
from fake_useragent import UserAgent
from random import choice, random
ua = UserAgent()
headers = {
    'user-agent': ua.random,
    'accept' : '*/*'
}
with open('file.txt', encoding='utf-8') as file:
    proxy_list = ''.join(file.readlines()).strip().split('\n')
def get_start_links():
    with open('final_1.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(
            (
                'Артикул',
                'Название',
                'Ссылка на товар',
                'Цена в гривнах'
            )
        )
    urls = []
    excel_data_df = pandas.read_excel(r'D:\Practise Python\Practise_parsing\prom_ua\Парсинг 100.xlsx', sheet_name='Лист1')
    exceles = excel_data_df['Группы'].tolist()
    hrefs = excel_data_df['Назв'].tolist()
    iteration = 0
    for ex in exceles:
        if ex == 'Все группы':
            urls.append(hrefs[iteration])
              
        iteration += 1
        
    print(urls)
    print(len(urls))
    for url in urls[6:]:
        try:
            proxy = choice(proxy_list)
            proxies = {
                'http' : f'http://{proxy}'
            }
            req = requests.get(url = url, headers=headers, proxies=proxies)
            soup = BeautifulSoup(req.text, 'lxml')
            collect_links = []
            links = [] 
            link = url.split('.html')[1]
            linky = url.split('.html')[0]

            for i in range(60, 9999):
                proxy_3 = choice(proxy_list)
                proxies = {
                    'http' : f'http://{proxy_3}'
                }
                full_page_link = f'{linky};{i}.html{link}'
                print(url)
                print(full_page_link)
                print('#' * 20)
                req = requests.get(url = full_page_link, headers=headers, proxies = proxies)
                soup = BeautifulSoup(req.text, 'lxml')
                
                cards = soup.find_all('div', class_ = '_3V+Tg nwC-g HgCCI zVmCi mhZIu PGRan _64+h- Qpejc')
                for card in cards:
                    try:
                        card = 'https://prom.ua'+card.find('a', class_ = '_6zoki sYTuN').get('href')
                        card = card.split('?')[0]
                        if card in links: 
                            full_page_link = f'{linky};1.html{link}'
                            break
                        else:
                            links.append(card)
                        
                        proxy_4 = choice(proxy_list)
                        proxies = {
                            'http' : f'http://{proxy_4}'
                        }
                        response = requests.get(url = card, headers=headers, proxies = proxies)
                        soup = BeautifulSoup(response.text, 'lxml')
                        
                        title = soup.find('h1', class_ = '_0sHg4 +XUmw _7E9WI Lb6YM').text.strip()
                        try:
                            articul = soup.find('span', {'data-qaid' : 'product-sku'}).text.strip()
                            articul = articul.split(': ')[-1]
                        except:
                            articul = None
                        price = soup.find('span', {'data-qaid' : 'product_price'}).find('span', class_ = '_0sHg4 cFWgH').text.strip() 
                        with open('final_1.csv', 'a', encoding='utf-8') as file:
                            writer = csv.writer(file, delimiter = ',')
                            writer.writerow(
                                (
                                    articul,
                                    title, 
                                    card, 
                                    price
                                )
                            )        
                    except:
                        print('None')
                        continue
                                
                if full_page_link in collect_links:
                    break
                else:
                    collect_links.append(full_page_link)
                        
        except:
            print('Нельзя')


               




def main():
    get_start_links()
    # get_data(file_path=r'D:\Practise Python\Practise_parsing\prom_ua\data\all_links2.txt')
    
    
if __name__ == '__main__':  
    main()