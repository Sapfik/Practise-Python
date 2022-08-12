import requests 
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time


def get_first_news ():
    headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    url = 'https://www.securitylab.ru/news/'
    r = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    article_cards = soup.find_all('a' , class_ = 'article-card')
    news_dict = {}
    for article in article_cards:
        article_title = article.find('h2' , class_ = 'article-card-title').text.strip()
        article_description = article.find('p').text.strip()
        article_link = 'https://www.securitylab.ru' + article.get('href')
       
        article_date_time = article.find('time').get('datetime')
        date_from_iso = datetime.fromisoformat(article_date_time)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S") 
        #%Y-%m-%d %H:%M:%S ---> %Y - YEARS, %m - months, %d - days, %H - hours, %M - minuets, %S - seconds 
        article_date_timestep = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

        article_id = article_link.split('/')[-1]
        article_id = article_id[:-4]

        # print(f'{article_title} | {article_link} | {article_date_timestep}')

        news_dict[article_id] = {
            'article_date_time_step' : article_date_timestep,
            'article title' : article_title,
            'article description' : article_description, 
            'article link' : article_link
        }

    with open('news_dict.json', 'w', encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    
    # Читаем из файла все, что там есть
    with open ('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)
    
    # Делаем запросы на получения данных карточках, которые имеются
    headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    url = 'https://www.securitylab.ru/news/'
    r = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    article_cards = soup.find_all('a' , class_ = 'article-card')

    fresh_news = {}
    
    # Проходимся по списку карточек, которые есть
    for article in article_cards:
        article_link = 'https://www.securitylab.ru' + article.get('href')
        article_id = article_link.split('/')[-1]
        article_id = article_id[:-4]
        
        # Если id есть в подгружаем словаре, то продолжаем
        if article_id in news_dict:
            continue

        # Собираем все данные, которые не лежат в списке
        else:
            article_title = article.find('h2' , class_ = 'article-card-title').text.strip()
            article_description = article.find('p').text.strip()
        
            article_date_time = article.find('time').get('datetime')
            date_from_iso = datetime.fromisoformat(article_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S") 
            #%Y-%m-%d %H:%M:%S ---> %Y - YEARS, %m - months, %d - days, %H - hours, %M - minuets, %S - seconds 
            article_date_timestep = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())
            
            # Заносим новые данные в словарь
            news_dict[article_id] = {
                'article_date_time_step' : article_date_timestep,
                'article title' : article_title,
                'article description' : article_description, 
                'article link' : article_link
            }

            fresh_news[article_id] = {
                'article_date_time_step' : article_date_timestep,
                'article title' : article_title,
                'article description' : article_description, 
                'article link' : article_link
            }

    with open ('news_dict.json', 'w',encoding='utf-8') as file:
        json.dump(news_dict, file, indent = 4, ensure_ascii=False)
    
    return fresh_news    



def main():        
    # get_first_news()
    check_news_update()

if __name__ == '__main__':
    main()