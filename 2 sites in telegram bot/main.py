import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

def get_all_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    
    url = 'https://www.securitylab.ru/news/'
    req = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    
    all_cards = soup.find_all('a', class_ = 'article-card')
    news_dict = {}
    for card in all_cards:
        title = card.find('h2', class_ = 'article-card-title').text.strip()
        card_description = card.find('p').text.strip()
        card_link = 'https://www.securitylab.ru' + card.get('href')
        
        card_time = card.find('time').get('datetime')
        date_from_iso = datetime.fromisoformat(card_time)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
        card_date = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())
        
        card_id = card_link.split('/')[-1]
        card_id = card_id[:-4]
        news_dict[card_id] = {
            'Date Time' : card_date,
            'Title' : title,
            'Card description' : card_description,
            'Link' : card_link
        }
        
    # with open('news_dict.json', 'w', encoding='utf-8') as file:
    #     json.dump(news_dict, file, indent=4, ensure_ascii=False)
        
        
    url = 'https://hi-tech.news/'
    response = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    article_cards = soup.find_all('div', class_ = 'post-body')
    articles_dict = {}
    for article in article_cards:
        article_title = article.find('div', class_ = 'post-content').find('div', class_ ='title').text.strip()
        article_description = article.find('div', class_ = 'the-excerpt').text.strip()
        article_link = article.find('a', class_ = 'post-title-a').get('href')  
        
        article_time = article.find('div',class_ = 'post-detail pd-padding').find('a').text.strip()
        
        article_id  = article_link.split('/')[-1]
        article_id = article_id[:4]
        
        articles_dict[article_id] = {
            'Date time' : article_time,
            'Title' : article_title,
            'Description' : article_description, 
            'Link' : article_link
        }
        
    with open('article_dict.json', 'w', encoding='utf-8') as file:
        json.dump(articles_dict, file, indent=4, ensure_ascii=False)
        
    

def check_news():
    with open ('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    
    url = 'https://www.securitylab.ru/news/'
    req = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    
    all_cards = soup.find_all('a', class_ = 'article-card')
    fresh_news = {}
    
    for card in all_cards:
        card_link = 'https://www.securitylab.ru' + card.get('href')
        card_id = card_link.split('/')[-1]
        card_id = card_id[:-4]
        
        if card_id in news_dict:
            continue
        
        else:
            title = card.find('h2', class_ = 'article-card-title').text.strip()
            card_description = card.find('p').text.strip()
            
            card_time = card.find('time').get('datetime')
            date_from_iso = datetime.fromisoformat(card_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
            card_date = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())
            
            news_dict[card_id] = {
            'Date Time' : card_date,
            'Title' : title,
            'Card description' : card_description,
            'Link' : card_link
            }
            
            fresh_news[card_id] = {
            'Date Time' : card_date,
            'Title' : title,
            'Card description' : card_description,
            'Link' : card_link
            }
    
    with open('news_dict.json', 'w', encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
            
    return fresh_news


def check_news_hi_tech():
    with open('article_dict.json', encoding='utf-8') as file:
        article_dict = json.load(file)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    
    url = 'https://hi-tech.news/'
    req= requests.get(url = url, headers= headers)
    soup = BeautifulSoup(req.text, 'lxml')
    
    article_cards = soup.find_all('div', class_ = 'post-body')
    fresh_news_hi_tech  = {}
    
    for article in article_cards:
        article_link = article.find('a', class_ = 'post-title-a').get('href')
        article_id  = article_link.split('/')[-1]
        article_id = article_id[:4]
        
        if article_id in article_dict:
            continue
        
        else:
            article_title = article.find('div', class_ = 'post-content').find('div', class_ ='title').text.strip()
            article_description = article.find('div', class_ = 'the-excerpt').text.strip()
            article_time = article.find('div',class_ = 'post-detail pd-padding').find('a').text.strip()
            
            article_dict[article_id] = {
            'Date time' : article_time,
            'Title' : article_title,
            'Description' : article_description, 
            'Link' : article_link
            }
            
            fresh_news_hi_tech[article_id] = {
            'Date time' : article_time,
            'Title' : article_title,
            'Description' : article_description, 
            'Link' : article_link
            }
            
    with open('article_dict.json', 'w', encoding='utf-8') as file:
        json.dump(article_dict, file, indent=4, ensure_ascii=False)
        
    return fresh_news_hi_tech
        
    
    
def main():
    # get_all_news()
    check_news()
    check_news_hi_tech()
    
if __name__ == '__main__':
    main()