from wsgiref import headers
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'accept' : '*/*'
}

def getdata(url):
    req = requests.get(url = url, headers=headers)
    print(req.content)

def main():
    getdata(url = 'https://www.amazon.com/s?k=videocards&crid=3OLZE764CLM94&sprefix=videocards%2Caps%2C236&ref=nb_sb_noss')
    
if __name__ == '__main__':
    main()