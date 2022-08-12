import re

def convert_link(url):
    if 'https://www.' in url:
        url = url.replace('https://www.', '')
        
    elif 'https://' in url:
        url = url.replace('https://', '')
        
    elif 'http://' in url:
        url = url.replace('http://', '')
        
    elif 'www.' in url:
        url = url.replace
    elif 'http://www.' in url:
        url = url.replace('http://www.', '')
    domain = url.split('.')[0]
    print(domain)


convert_link(url = 'https://heroesempires.com/')
