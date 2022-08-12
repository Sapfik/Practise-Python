import requests
import json
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'accept' : '*/*'
}

def get_data(url):
    links = []
    response = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    all_links = soup.find_all('a', class_ = 'link-relatedcategory cat-36 inlblk tdnone icon-link')
    for link in all_links:
        link = link.get('href')
        links.append(link)
        
    with open('start_links.txt', 'w', encoding='utf-8') as file:
        for link in links:
            file.write(f'{link}\n')
        

def get_data_from_links(file_path):
    result = []
    with open(file_path, encoding='utf-8') as file:
        urls = [line.strip() for line in file.readlines()]
        
    for url in urls[:1]:
        req = requests.get(url = url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        
        cards = soup.find_all('div', class_ = 'offer-wrapper')
        count = 1
        for card in cards[:10]:
            title = card.find('h3', class_ = 'lheight22 margintop5').text.strip()
            if card.find('a', class_ = 'marginright5 link linkWithHash detailsLink'):
                card_link = card.find('a', class_ = 'marginright5').get('href')
            else:
                card_link = card.find('a', class_ = 'marginright5 link linkWithHash detailsLink linkWithHashPromoted').get('href')
            try:
                price = card.find('p', class_ = 'price').get_text(strip=True)
            except:
                price = '----'
            date = card.find('p', class_ = 'lheight16').text.strip()
            try:
                card_image = card.find('img', class_ = 'fleft').get('src')
            except:
                continue
            
            r = requests.get(url = card_image, headers=headers)
            with open(f'data/{count}.jpg', 'wb') as file:
                file.write(r.content)
            
            result.append(
                {
                    'title' : title,
                    'link' : card_link,
                    'price' : price,
                    'number of image' : f'{count}.jpg'
                }
            )
            
            count += 1
    
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

def main():
    get_data(url = 'https://www.olx.ua/')
    get_data_from_links(file_path='D:\Practise Python\Practise_parsing\Parse_OLX\start_links.txt')
    
if __name__ == '__main__':
    main()