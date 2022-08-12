from imp import reload
from wsgiref import headers
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from requests_html import HTMLSession
from selenium import webdriver

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'accept' : '*/*'
}

def get_first_links(url):
    # s = HTMLSession()
    
    # r = s.get(url = url, headers=headers)
    # script = req.text
    # print(script)
    # r.html.render(script=script, reload=False)
    # print(r.html.html)
    # soup = BeautifulSoup(r.html.html, 'html.parser')
    # req = requests.get(url = url , headers = headers)
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(r.html.html)
        
    # link = r.html.find('department-menu__link _6lGWx _2Z98f')
    # print(link)
    # soup = BeautifulSoup(req.text, 'lxml')
    
    # links = soup.find_all('a' ,class_ = 'department-menu__link _6lGWx _2Z98f')
    # for link in links:
    #     print(link)
    
    
    driver = webdriver.Chrome(executable_path=r'D:\Practise Python\Practise_parsing\Kogan_parse\chromedriver.exe')
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    button = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]')
    button.click()
    time.sleep(200)
    # with open('data/first_page.html', 'w', encoding='utf-8') as file:
    #     file.write(driver.page_source)
    # with open('data/first_page.html', encoding='utf-8') as file:
    #     src = file.read()
        
    

def main():
    get_first_links(url = 'https://www.kogan.com/au/')
    
if __name__ == '__main__':
    main()