import requests
from bs4 import BeautifulSoup
import time
import datetime
import json
import os
import csv

def get_all_pages():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'accept' : '*/*'
    }
    # req = requests.get(url = 'https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/', headers=headers)
    
    # if not os.path.exists('data'):    # Если наша папка с проектом не содержит папки с именем data, то мы её создаем
    #     os.mkdir('data')
        
    # with open('data/page_1.html' , 'w', encoding='utf-8') as file:
    #     file.write(req.text)
    
    with open('data/page_1.html', encoding='utf-8') as file:
        src = file.read()
        
    soup = BeautifulSoup(src, 'lxml')
    pages_count  = int(soup.find('div', class_ = 'bx-pagination-container').find_all('a')[-2].text)
    
    for i in range(1, pages_count + 1):
        url = f'https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?PAGEN_1={i}'
        
        req = requests.get(url = url, headers=headers)
            
        with open(f'data/page_{i}.html', 'w', encoding='utf-8') as file:
            file.write(req.text)
            
        time.sleep(2)
        
    return pages_count + 1
                    

def collect_data(pages_count):
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y")
    data = []
    
    with open(f'data_{cur_time}.csv', 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(
            (
                'Название',
                'Цена',
                'Ссылка'
            )
        )
    
    for page in range(1, pages_count):
        with open(f'data/page_{page}.html', encoding='utf-8') as file:
            src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            all_cards_links = soup.find_all('a', class_ = 'product-item__link')
            for link in all_cards_links:
                article_title = link.find('p', class_ = 'product-item__articul').text.strip()
                article_price = link.find('p', class_ = 'product-item__price').text.lstrip('руб. ')    
                link = 'https://shop.casio.ru'+link.get('href')
                print(f'Title: {article_title}\nPrice: {article_price}\nLink: {link}')
                print('#' * 20)
                
                data.append(
                    {
                        'article_title' : article_title,
                        'article_price' : article_price,
                        'article_link' : link
                    }
                )
                
                with open(f'data_{cur_time}.csv', 'a', encoding='cp1251') as file:
                    writer = csv.writer(file, delimiter = ';')
                    writer.writerow(
                        (
                            article_title,
                            article_price,
                            link
                        )
                    )
                
        print(f'[INFO]  Обработано {page} / 5')
        
    with open(f'data_{cur_time}.json', 'w', encoding='utf-8') as file:
        json.dump(data , file, indent=4, ensure_ascii=False)
        

def main():
    pages_count = get_all_pages()
    collect_data(pages_count=pages_count)
    
    
if __name__ == '__main__':
    main()