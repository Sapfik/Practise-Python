import requests 
from bs4 import BeautifulSoup
import time

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'accept' : '*/*'
}

def get_content(url):
    pass

def main():
    get_content(url = 'https://www.ukrinform.ua/block-lastnews')
    
if __name__ == '__main__':
    main()