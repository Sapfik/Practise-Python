import sqlite3
import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    'User-Agent': ua.random,
    'accept' : '*/*'
}

def get_data(url):
    sql = sqlite3.connect('countries.sqlite')
    cursor = sql.cursor()

    req = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    
    russion_title = soup.find('table', class_ = 'als-sortable-table').find('tbody').find_all('tr')
    for r_l in russion_title:
        title = r_l.find_all('td')[0].text.strip()
        english_lan = r_l.find_all('td')[2].text.strip()
        alpha2 = r_l.find_all('td')[3].text.strip()
        cursor.execute("""
            INSERT INTO countries (russion_text,english_text,symbols_text) VALUES(?, ?, ?)              
        """, (title, english_lan, alpha2))
        sql.commit()
    



def main():
    get_data(url = 'https://www.artlebedev.ru/country-list/')
    
if __name__ == '__main__':
    main()