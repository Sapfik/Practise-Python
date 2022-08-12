from enum import EnumMeta
import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    'user-agent' : ua.random,
    'accept'  : '*/*'
}

def get_first_links(url):
    req = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(req.text,'lxml')
    
    links = soup.find_all('a', class_ = 'main-popular__category')
    for link in links:
        link  = 'https://www.kuchenland.ru' + link.get('href')
        with open('first_links.txt', 'a', encoding='utf-8') as file:
            file.write(f'{link}\n')
            

def get_second_links(file_path):
    with open(file_path, encoding='utf-8') as file:
        urls = [line.strip() for line in file.readlines()]

    for url in urls:
        response = requests.get(url = url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        links = soup.find_all('div', class_ = 'new_main-popular__block--link')
        for link in links:
            link = 'https://www.kuchenland.ru' + link.find('a').get('href')
            with open('second_links.txt', 'a', encoding='utf-8') as file:
                file.write(f'{link}\n')
            

def get_data(file_path):
    with open(file_path, encoding='utf-8') as file:
        urls = [line.strip() for line in file.readlines()]
    
    for url in urls:
        response = requests.get(url = url, headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        try:
            pagination = int(soup.find('div', class_ = 'pagination catalog__pagination').find_all('a', class_ = 'pagination__button')[-1].text.strip())
            for page in range(1, pagination + 1):
                u = f'{url}?PAGEN_1={page}'
                req = requests.get(url = u, headers=headers)
                soup = BeautifulSoup(req.text,'lxml')
                
                card_links = soup.find_all('span', class_ = 'item-block__name')
                for card_link in card_links:
                    card_link = 'https://www.kuchenland.ru' + card_link.find('a').get('href')
                    with open('card_links.txt', 'a', encoding='utf-8') as file:
                        file.write(f'{card_link}\n')               
                
        except:
            req = requests.get(url = url, headers=headers)
            soup = BeautifulSoup(req.text,'lxml')
            
            card_links = soup.find_all('span', class_ = 'item-block__name')
            for card_link in card_links:
                card_link = 'https://www.kuchenland.ru' + card_link.find('a').get('href')
                with open('card_links.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{card_link}\n')



def get_data_from_cards(file_path):
    with open('result.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(
            (
                'Ссылка на фото',
                'Ссылка',
                'Название',
                'Описание',
                'Цена',
                'Артикул',
                'Категория',
                'Подкатегория 1',
                'Подкатегория 2',
                'Подкатегория 3'
            )
        )
    with open(file_path, encoding='utf-8') as file:
        urls = [line.strip() for line in file.readlines()]
    
    for url in urls:
        response = requests.get(url = url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        title = soup.find('h1', class_ = 'item-detail__title').text.strip()
        price = soup.find('div', class_ = 'item-detail__price-current').text.strip()
        articul = soup.find('div', class_ = 'item-detail__row item-detail__row--line').text.strip()
        articul = articul.split('Артикул:')[-1].split('                    ')[-1]
        description = soup.find('div', class_ = 'description-block__text').text.strip()
        image = 'https://www.kuchenland.ru' + soup.find('img', class_ = 'js-drift-img').get('src')
        categorie = soup.find_all('li', class_ = 'breadcrumbs__item')[4].text.strip()
        under_categorie_1 = soup.find_all('li', class_ ='breadcrumbs__item')[6].text.strip()
        under_categorie_2 = soup.find_all('li', class_ = 'breadcrumbs__item')[8].text.strip()
        under_categorie_3 = soup.find_all('li', class_ = 'breadcrumbs__item')[10].text.strip()
        with open('result.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(
                (
                    image,
                    url,
                    title,
                    description,
                    price,
                    articul,
                    categorie,
                    under_categorie_1,
                    under_categorie_2,
                    under_categorie_3
                )
            )    


def main():
    # get_first_links(url = 'https://www.kuchenland.ru/catalog/')
    # get_second_links(file_path = r'D:\Practise Python\Practise_parsing\parse_ Kuhenland\first_links.txt')
    # get_data(file_path=r'D:\Practise Python\Practise_parsing\parse_ Kuhenland\second_links.txt')
    get_data_from_cards(file_path=r'D:\Practise Python\Practise_parsing\parse_ Kuhenland\card_links.txt')
if __name__ == '__main__':
    main()