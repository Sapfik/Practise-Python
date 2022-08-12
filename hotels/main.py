
import requests
from bs4 import BeautifulSoup
import csv
import re
from selenium import webdriver
import time

from requests.sessions import should_bypass_proxies

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'accept' : '*/*'
}

def get_pages(url):
    links = []
    with open ('result.csv', 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(
            (
                'Ссылка',
                'Имя',
                'Название отеля',
                'Номер телефона',
                'Почта'
            )
        )
    s = requests.Session()
    req = s.get(url = url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    
    pages_count = int(soup.find('div', class_ = 'P-FloatL P-480-FloatNone').find_all('a')[-2].text)
    for page in range(1, pages_count+1):
        url = f'https://propertysearch.hicentral.com/HBR/ForSale/?/Results/HotSheet/d/{page}//'
        
        response = s.get(url = url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        card_links = soup.find_all('li', class_ = 'P-Active')
        for link in card_links:
            link = 'https://propertysearch.hicentral.com/HBR/ForSale/'+link.find('a', class_ = 'P-FloatL P-PhotoList P-480-FloatNone').get('href')
            links.append(link)
    count = 1        
    for link in links:
        r = s.get(url = link, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find('span', class_ = 'realtor-name').text.strip()
        licens = soup.find('span', class_ = 'realtor-license').find_next('em').text.strip()
        try:
            driver = webdriver.Chrome(executable_path='D:\Practise Python\Practise_parsing\hotels\chromedriver.exe')
            driver.get(link)
            time.sleep(5)
            
            phone = driver.find_element_by_xpath('/html/body/div/div/section/div[2]/form/div[2]/aside/div[1]/div[2]/p[2]/a[1]').get_attribute('href')
            new_number = phone.split(':')[-1]
            e_mail = driver.find_element_by_xpath('/html/body/div[1]/div/section/div[2]/form/div[2]/aside/div[1]/div[2]/p[2]/a[2]').get_attribute('href')
            new_url = e_mail.split('?')[0]
            new1_url = new_url.split(':')[-1]
            
            with open('result.csv', 'a', encoding='cp1251') as file:
                writer = csv.writer(file, delimiter = ';')
                writer.writerow(
                    (
                        link,
                        title,
                        licens,
                        new_number,
                        new1_url
                    )
                )

        
        except Exception as ex:
            print(ex)
            
        finally:
            driver.close()
            driver.quit()


def main():
    get_pages(url = 'https://propertysearch.hicentral.com/HBR/ForSale/?/Results/HotSheet/d///')
    
if __name__ == '__main__':
    main()