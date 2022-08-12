import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'accept' : '*/*'
}

def get_content(link):
    # url = 'https://www.youtube.com/'
    req = requests.get(url = link, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    
    cards = soup.find_all('div', class_ = 'style-scope')
    for card in cards:
        linky = card.find('a', class_ = 'yt-simple-endpoint').get('href')
        print(linky)
    
def main():
    get_content(link = 'https://www.youtube.com/results?search_query=%D0%BA%D0%B0%D0%BA+%D1%81%D0%B2%D0%B0%D1%80%D0%B8%D1%82%D1%8C+%D0%BC%D0%B0%D0%BA%D0%B0%D1%80%D0%BE%D0%BD%D1%8B+')
    
if __name__  == '__main__':
    main()
    

