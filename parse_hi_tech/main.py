import requests
from bs4 import BeautifulSoup
import json

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'accept':'*/*'
}

def get_articles_urls(url):
    s = requests.Session()
    req = s.get(url = url, headers=headers)
    
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(req.text)
    articles_url_list = []
    soup = BeautifulSoup(req.text, 'lxml')
    pagination_count = int(soup.find('span', class_ = 'navigations').find_all('a')[-1].text.strip())
    for page in range(1,pagination_count+1):
        response = s.get(url=f"https://hi-tech.news/page/{page}/")
        soup = BeautifulSoup(response.text, 'lxml')
        
        articles_urls = soup.find_all('a', class_ = 'post-title-a')
        
        for au in articles_urls:
            article_url = au.get('href')
            articles_url_list.append(article_url)
        
        print(f"{page} / {pagination_count}")
            
        with open('articles_list.txt', 'w', encoding='utf-8') as file:
            for url in articles_url_list:
                file.write(f"{url}\n")
                

def get_data(file_path):
    with open(file_path, encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]     #file.readlines() -  читает каждую строку в файле
        
    s = requests.Session()
    result_list = []
    
    for url in enumerate(urls_list):
        response = s.get(url = url[1], headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        article_title = soup.find('h1', class_ = 'title').text.strip()
        article_date = soup.find('div', class_ = 'tile-meta').find('div', class_ = 'tile-views').text.strip()
        article_image = 'https://hi-tech.news' + soup.find('div', class_ = 'post-media-full').find('img').get('src')
        article_text = soup.find('div', class_ = 'the-excerpt').text.strip()
        
        result_list.append(
            {
                'original url' : url[1],
                'article title' : article_title,
                'article date' : article_date,
                'article image' : article_image,
                'article text' : article_text  
            }
            
        )
        
        print(f'Обработал {url[0] + 1} / {urls_list}')
        
    with open('result_list.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)


def main():
    # get_articles_urls('https://hi-tech.news/')
    get_data('articles_list.txt')
    
if __name__ == '__main__':
    main()