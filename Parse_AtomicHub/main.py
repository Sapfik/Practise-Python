from email import header
from lib2to3.pgen2 import driver
from bs4 import BeautifulSoup
from matplotlib.pyplot import get
import requests 
from selenium import webdriver
import time


headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'accept' : '*/*'
}

def get_data(url):
    links = []
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')   #Экран в фоновом режиме
    # options.headless = True 
    driver = webdriver.Chrome(executable_path=r'D:\Practise Python\Practise_parsing\Parse_AtomicHub\chromedriver.exe', options=options)
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    
    button_collection = driver.find_elements_by_class_name('menu-option')[1]
    button_collection.click()
    time.sleep(7)
    
    button_popularity = driver.find_element_by_class_name('dropdown-toggle')
    button_popularity.click()
    time.sleep(5)
    
    button_newest = driver.find_elements_by_class_name('dropdown-item')[3]
    button_newest.click()
    time.sleep(10)
    
    button_notwl = driver.find_elements_by_class_name('checkbox-input')[0]
    button_notwl.click()
    time.sleep(10)
    
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
        driver.close()
        driver.quit()
        
    with open('index.html', 'r', encoding='utf-8') as file:
        src  = file.read()
        
    soup = BeautifulSoup(src, 'lxml')
    all_links = soup.find_all('div', class_ = 'buttons')
    for link in all_links:
        link = 'https://wax.atomichub.io' + link.find('a')['href']
        with open('links.txt', 'a', encoding='utf-8') as file:
            file.write(f'{link}\n')
    # links = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[7]/div/div[1]/div[2]/div[2]/a').get_attribute('href')
    # print(links)
    # links = driver.find_elements_by_class_name('CollectionCard large-card')
    # for link in links:
    #     link = link.find_element_by_class_name('buttons').get_attribute('href')
    #     print(link)
    
def get_content(file_path):
    with open(file_path, encoding='utf-8') as file:
        urls = [line.strip() for line in file.readlines()]
    
    print(urls)
    
def main():
    get_data('https://wax.atomichub.io/explorer')
    get_content(file_path=r'D:\Practise Python\Practise_parsing\Parse_AtomicHub\links.txt')
    
if __name__ == '__main__':
    main()