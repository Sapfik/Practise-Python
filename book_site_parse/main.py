import requests
from bs4 import BeautifulSoup
import json
import re

headers= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'accept' : '*/*'
}

def get_data(url):
    req = requests.get(url = url, headers=headers)
    # with open('index.html' , 'w', encoding='utf-8') as file:
    #     file.write(req.text)

    soup = BeautifulSoup(req.text, 'lxml')
    pages_count = int(soup.find('div', class_= 'pagination').find_all('li')[-2].text)
    
    
    with open('pages.txt', 'w', encoding='utf-8') as file:
        value = 1
        for page in range(1, pages_count+1):
            url = f'https://www.bambook.com/catalogue/ua/knigi?vs={value}&ord=3+desc&rid=10'
            value += 24
            file.write(f"{url}\n")
            
            
def collect_links(file_path):
    all_links = []
    
    with open(file_path, encoding='utf-8') as file:
        pages_list = [line.strip() for line in file.readlines()]
        
    for url in pages_list[:10]:
        req = requests.get(url = url, headers = headers)
        soup = BeautifulSoup(req.text, 'lxml')
        all_card_links  = soup.find_all('a', class_ = 'name')
        for url in all_card_links:
            url = 'https:'+url.get('href')
            all_links.append(url)
        
    with open('all_links.txt', 'w', encoding='utf-8') as file:
        for link in all_links:
            file.write(f"{link}\n")
            

def collect_data(file_path):
    result_data = {}
    
    with open(file_path, encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]
        
    for url in urls_list:
        req = requests.get(url = url, headers = headers)
        soup = BeautifulSoup(req.text, 'lxml')
        
        try:
            title = soup.find('h1', class_ = 'card-title').text.strip()
        except:
            title = None
            
        try:
            author = soup.find(text = re.compile('Автор')).find_next().text.strip()
        except:
            author = None
            
        try:
            pages = soup.find(text = re.compile('Сторiнок')).find_next().text.strip()
        except:
            pages = None
            
        try:
            date_start = soup.find(text = re.compile('Рік видання')).find_next().text.strip()
        except:
            date_start = None
            
        try:
            language = soup.find(text = re.compile('Мова')).find_next().text.strip()
        except:
            language = None
        
        try:
            genre = soup.find(text = re.compile('Жанр')).find_next().find_all('a')
            for g in genre:
                all_genre = g.text.strip()
        except:
            genre = None
            
        try:
            place_from = soup.find(text = re.compile('Місце видання')).find_next().text.strip()
        except:
            place_from = None
            
        try:
            price = soup.find('div', class_ = 'new-price').text.strip()
        except:
            price  = None
            
        print(price)
            
            
        id= url.split('-')[-1]
        
        result_data[id] = {
            'Название' : title,
            'Цена' : price,
            'Автор' : author,
            'Количество страниц' : pages,
            'Год издания' : date_start,
            'Язык' : language,
            'Жанр' : all_genre,
            'Место выдачи' : place_from,
        }
        
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)
               
            


def main():
    # get_data(url = 'https://www.bambook.com/catalogue/ua/knigi')
    # collect_links(file_path='pages.txt')
    collect_data(file_path = 'all_links.txt')
    
if __name__ == '__main__':
    main()