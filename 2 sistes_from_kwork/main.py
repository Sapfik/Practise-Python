import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(executable_path=r'D:\Practise Python\Practise_parsing\2 sistes_from_kwork\chromedriver.exe')

url = 'https://truck.av.by/filter?brands[0][brand]=44&brands[0][year][min]=2007&brands[1][brand]=609&brands[1][year][min]=2007&brands[2][brand]=683&brands[2][model]=5246&brands[2][year][min]=2007&brands[3][brand]=1104&brands[3][year][min]=2007&brands[4][brand]=1238&brands[4][year][min]=2007&brands[5][brand]=1039&brands[5][model]=5597&brands[5][year][min]=2007&brands[6][brand]=480&brands[6][model]=523&brands[6][year][min]=2012&brands[7][brand]=683&brands[7][model]=5188&brands[7][year][min]=2007&place_country=1&page=13&sort=4'

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'accept' : '*/*'
}

def get_data():
    result = []
    result_dict = {}
    driver.get('https://truck.av.by/filter?brands[0][brand]=44&brands[0][year][min]=2007&brands[1][brand]=609&brands[1][year][min]=2007&brands[2][brand]=683&brands[2][model]=5246&brands[2][year][min]=2007&brands[3][brand]=1104&brands[3][year][min]=2007&brands[4][brand]=1238&brands[4][year][min]=2007&brands[5][brand]=1039&brands[5][model]=5597&brands[5][year][min]=2007&brands[6][brand]=480&brands[6][model]=523&brands[6][year][min]=2012&brands[7][brand]=683&brands[7][model]=5188&brands[7][year][min]=2007&place_country=1&page=13&sort=4')
    time.sleep(5)
    driver.maximize_window()
    count = 13
    while True:
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/main/div/div/div[1]/div[4]/div[3]/div/div[2]/div/div[1]/a').click()

            time.sleep(3)     
            count += 1  
        except:
            break
    

    
    last_card = driver.find_elements_by_class_name('listing-item')[-1]
    actions = ActionChains(driver)
    actions.move_to_element(last_card).perform()
    
    all_cards = driver.find_elements_by_class_name('listing-item__link')
    for link in all_cards:
        url_link = link.get_attribute('href')
        result.append(url_link)
    

    for url in result:
        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml') 

        title = soup.find('h1', class_ = 'card__title').text.strip()
        new_title = title.split(',',2)[0].split("Продажа")[1]
        price = soup.find('div', class_ = 'card__price-primary').text.strip()
        text = soup.find('div', class_ = 'card__params').text.strip()
        new_year = text.split(",",2)[0]
        try:
            mileage = text.split(",",8)[-1]
            car = text.split(",",8)[3]
        except:
            mileage = text.split(",",6)[-1]
            car = text.split(",",8)[1]
            
        item_link = url.split("/")[-1]

        result_dict[item_link] = {
            'title' : new_title,
            'price' : price,
            'year' : new_year,
            'mileage' : mileage,
            'link' : url
        }
        
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_dict, file, indent=4, ensure_ascii=False)


def check_data():
    with open('result.json', encoding='utf-8') as file:
        result_dict = json.load(file)
    
    result = []
    result_dic = {}
    fresh_dict = {}
    driver.get('https://truck.av.by/filter?brands[0][brand]=44&brands[0][year][min]=2007&brands[1][brand]=609&brands[1][year][min]=2007&brands[2][brand]=683&brands[2][model]=5246&brands[2][year][min]=2007&brands[3][brand]=1104&brands[3][year][min]=2007&brands[4][brand]=1238&brands[4][year][min]=2007&brands[5][brand]=1039&brands[5][model]=5597&brands[5][year][min]=2007&brands[6][brand]=480&brands[6][model]=523&brands[6][year][min]=2012&brands[7][brand]=683&brands[7][model]=5188&brands[7][year][min]=2007&place_country=1&page=13&sort=4')
    time.sleep(5)
    driver.maximize_window()
    while True:
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/main/div/div/div[1]/div[4]/div[3]/div/div[2]/div/div[1]/a').click()
            time.sleep(3)      
        except:
            break
    
    
    last_card = driver.find_elements_by_class_name('listing-item')[-1]
    actions = ActionChains(driver)
    actions.move_to_element(last_card).perform()
    
    all_cards = driver.find_elements_by_class_name('listing-item__link')
    for link in all_cards:
        url_link = link.get_attribute('href')
        result.append(url_link)
    
    print(result)
    
    for url in result:
        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        
        item_link = url.split('/')[-1]
        if item_link in result_dict:
            continue
        
        else:
            title = soup.find('h1', class_ = 'card__title').text.strip()
            new_title = title.split(',',2)[0].split("Продажа")[1]
            price = soup.find('div', class_ = 'card__price-primary').text.strip()
            text = soup.find('div', class_ = 'card__params').text.strip()
            new_year = text.split(",",2)[0]
            try:
                mileage = text.split(",",8)[-1]
                car = text.split(",",8)[3]
            except:
                mileage = text.split(",",6)[-1]
                car = text.split(",",8)[1]
                
            result_dict[item_link] = {
            'title' : new_title,
            'price' : price,
            'year' : new_year,
            'mileage' : mileage,
            'link' : url
            }
            
            fresh_dict[item_link] = {
            'title' : new_title,
            'price' : price,
            'year' : new_year,
            'mileage' : mileage,
            'link' : url
            }
            
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_dict, file, indent = 4, ensure_ascii=False)
    
    return fresh_dict            


def main():
    # get_data()
    check_data()
    
if __name__ == '__main__':
    main()
