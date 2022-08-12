import requests
from bs4 import BeautifulSoup
from random import randrange
import time
import json

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'accept' : '*/*'
}

article_urls_list = []

def get_articles(url):
    s = requests.Session()    # Session() - сохраняет запросы из сайта в куки
    response = s.get(url = url, headers=headers)
    
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text) 
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    pages_count = int(soup.find('span', class_ = 'navigations').find_all('a')[-1].text)
    for page in range(1, pages_count + 1):
    # for page in range(1, 2):
        url = f'https://hi-tech.news/page/{page}/'
        req = requests.get(url = url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        
        articles_urls = soup.find_all('a', class_ = 'post-title-a')
        for au in articles_urls:
            url = au.get('href')
            article_urls_list.append(url)
        
        time.sleep(randrange(2, 5))
        print(f'Обработал {page} / {pages_count}')
            
    with open('article_urls_list.txt', 'w', encoding='utf-8') as file:
        for u in article_urls_list:
            file.write(f'{u}\n')
            
    return 'Обработал все данные!'
        

def get_data(file_path):
    with open(file_path) as file:
        urls_list = [line.strip() for line in file.readlines()]    #Читает каждую строку в txt файле

    urls_count  = len(urls_list)
    s = requests.Session()
    result_list = []
    for url in enumerate(urls_list[:500]):    # enumerate - разбивает список по номеру и содержимому элемента
        response = s.get(url = url[1], headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        article_title = soup.find('h1', class_ = 'title').text.strip()
        article_date = soup.find('div' , class_ = 'post').find('div', class_ = 'tile-views').text.strip()
        article_image = 'https://hi-tech.news' + soup.find('div', class_ = 'post-media-full').find('img').get('src')
        article_text = soup.find('div', class_ = 'the-excerpt').text.strip().replace('\n', '')

        result_list.append(
            {
                'original_url' : url[1], 
                'article_title':article_title,
                'article_date': article_date,
                'article_image' : article_image,
                'article_text' : article_text
            }
        )
        
        print(f'{url[0] + 1}/{urls_count}')
        
    with open('result_list.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

def main():
    # get_articles(url='https://hi-tech.news/')
    get_data('article_urls_list.txt')
    
if __name__ == '__main__':
    main()