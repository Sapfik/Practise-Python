import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
import re
import wordninja

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'accept' : '*/*'
}

def get_link_products(url):
    product_link_list = []
    response = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    links = soup.find_all('a', class_ = 'vn-link vn-nav__link')
    for link in links:
        link = link.get('href')
        product_link_list.append(link)
    
    with open('product.txt', 'w', encoding='utf-8') as file:
        for link in product_link_list:
            file.write(f'{link}\n')
            
            
def get_all_categories(file_path):
    categorie_links_list = []
    with open(file_path, encoding='utf-8') as file:
        categories = [line.strip() for line in file.readlines()]
        
    for url in categories:
        req = requests.get(url = url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')  
        categorie_links = soup.find_all('a', class_ = 'vn-link')
        for categorie_link in categorie_links:
            categorie_link = categorie_link.get('href')
            if categorie_link in categorie_links_list:
                pass
            else:
                categorie_links_list.append(categorie_link)
    
    
            
    with open('categorie_links.txt', 'w', encoding='utf-8') as file:
        for link in categorie_links_list:
            file.write(f'{link}\n')
            

def get_data(file_path):
    new_and_last_links = []
    with open(file_path, encoding='utf-8') as file:
        all_links = [line.strip() for line in file.readlines()]
        
    for link in all_links:
        response = requests.get(url = link, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        if soup.find_all('a',class_ = 'vn-link vn__nav__link vn-3-grid-gap'):
            links = soup.find_all('a',class_ = 'vn-link vn__nav__link vn-3-grid-gap')
            for href in links:
                href = href.get('href')
                if href in new_and_last_links:
                    pass
                else:
                    new_and_last_links.append(href)
                
        else:
            new_and_last_links.append(link)
            
    
    with open('last_categorie_links.txt', 'w', encoding='utf-8') as file:
        for url in new_and_last_links:
            file.write(f'{url}\n')
        
 
def get_data_from_all_cards(file_path):
    urls = []
    with open(file_path, encoding='utf-8') as file:
        all_cards = [line.strip() for line in file.readlines()]
    
    for card in all_cards[:5]:
        req = requests.get(url = card, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        
        pagination = soup.find('div', class_ = 'catalog-product-list__total-count').text.strip()
        pagination = int(pagination.split('из ')[-1])
        if pagination % 24 != 0:
            pagination = pagination // 24
            pagination += 1
            
            
        if pagination % 24 == 0:
            pagination  = pagination // 24
            
        url = f'{card}?page={pagination}'
        urls.append(url)
        
    with open('pages.txt', 'w', encoding='utf-8') as file:
        for link in urls:
            file.write(f'{link}\n')
def get_from_pages_data(file_path):
    with open('result.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(
            (
                'Название',
                'Цена',
                'Описание',
                'Подробное описание',
                'Артикул',
                'Материалы',
                'Инструкция по использыванию',
                'Размер'    
            )
        )
    positions = []
    new_size = []
    result = []
    with open(file_path, encoding='utf-8') as file:
        urls = [line.strip() for line in file.readlines()]
    count = 1
    for url in urls:
        new_material = []
        # driver = webdriver.Chrome(executable_path='D:\Practise Python\Practise_parsing\Parse_ikea\chromedriver.exe')
        # driver.get(url)
        # with open(f'data/card_{count}.html', 'w', encoding='utf-8') as file:
        #     file.write(driver.page_source)
        #     driver.close()
        #     driver.quit()
        
        with open(f'data/card_{count}.html',  encoding='utf-8') as file:
            src = file.read()
        
        soup = BeautifulSoup(src, 'lxml')
        all_positions = soup.find_all('a', class_ = 'range-revamp-product-compact__wrapper-link')
        for position in all_positions:
            position = position.get('href')
            if position in positions:
                pass
            else:
                positions.append(position)
            
        for href in positions:
            req = requests.get(url = href, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')
            
            title = f"{soup.find('div', class_ = 'range-revamp-header-section__title--big notranslate').text.strip()} {soup.find('div', class_ = 'range-revamp-header-section__description').text.strip()}"
            price = soup.find('span', class_ = 'range-revamp-price__integer').text.strip()
            description = soup.find('div' , class_ = 'range-revamp-product-details__container').text.strip()
            description = description.split('Дизайнер')[0]
            articul = soup.find('span', class_ = 'range-revamp-product-identifier__value').text.strip()
            materials = soup.find('div', class_ = 'range-revamp-accordion__content').find_all('div', class_ = 'range-revamp-product-details__section')
            for material in materials:
                material = material.text.strip()
                new_material.append(material)
            count = 0
            for i in new_material:
                if i == new_material[0]:
                    new_mater = f"{i}"
                else:
                    new_mater += f" {new_material[count]}"
                count += 1
            
            try:
                
                instruction = soup.find('a', class_ = 'range-revamp-product-details__document-link').get('href')
            except:
                instruction = 'Нету'
            
            sizes = soup.find('div', class_ = 'range-revamp-product-dimensions__dimensions-container').find_all('p', class_ = 'range-revamp-product-dimensions__measurement-wrapper')
            for size in sizes:
                size = size.text.strip()
                new_size.append(size)
                
            count = 0
            for i in new_size:
                if i == new_size[0]:
                    new_s = f"{i}"
                else:
                    new_s += f" {new_size[count]}"
                count += 1
            try:
                just_description = soup.find('p', class_ = 'range-revamp-product-summary__description').text.strip()
            except:
                just_description = 'Нету описания'
              
            new_material = []
            new_size = []
            with open('result.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter = ';')
                writer.writerow(
                    (
                        title,
                        price,
                        just_description,
                        description,
                        articul,
                        new_mater,
                        instruction,
                        new_s
                    )
                )
            
            
        count += 1

        
        

def main():
    # get_link_products(url = 'https://www.ikea.com/ru/ru/cat/tovary-products/')
    # get_all_categories(file_path='D:\Practise Python\Practise_parsing\Parse_ikea\product.txt')
    # get_data(file_path= 'D:\Practise Python\Practise_parsing\Parse_ikea\categorie_links.txt')
    # get_data_from_all_cards(file_path='D:\Practise Python\Practise_parsing\Parse_ikea\last_categorie_links.txt')
    get_from_pages_data(file_path = 'D:\Practise Python\Practise_parsing\Parse_ikea\pages.txt')
if __name__ == '__main__':
    main()