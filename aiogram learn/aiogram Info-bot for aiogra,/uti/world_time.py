from wsgiref import headers
import requests
from bs4 import BeautifulSoup

def get_time(place):
    url = f'https://www.google.com/search?client=firefox-b-d&q=time+in+{place}'
    req = requests.get(url = url)
    soup = BeautifulSoup(req.text, 'lxml')
    parsed_time = soup.find_all('div', {'class': 'BNeawe iBp4i AP7Wnd'})[1].find_all(text=True, recursive=True)
    return parsed_time[0]
    
