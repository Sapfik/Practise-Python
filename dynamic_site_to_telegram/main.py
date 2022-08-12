import requests
import json
# Не импортируем bs4, так как на сайте есть json и с него будем вытягивать информацию

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'accept' : '*/*',
    'bx-ajax' : 'true'    # Для того, чтобы верно считывался json и не выдавал ошибку
}


def get_page(url):
    s = requests.Session()
    req = s.get(url= url, headers = headers)
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(req.text)
        
        
def get_json(url):
    s = requests.Session()
    req = s.get(url= url, headers = headers)
    
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(req.json(), file, indent=4, ensure_ascii=False)   #Читаем json на сайте
        
def get_collect():
    s = requests.Session()
    response = s.get(url = 'https://salomon.ru/catalog/muzhchiny/obuv/filter/size-is-10.5%20uk/apply/?PAGEN_1=1', headers=headers)
    
    result = []
    items_link = []
    data= response.json()
    
    pagination_count = data.get('pagination').get('pageCount')
    
    for page_count in range(1, pagination_count+1):
        url = f'https://salomon.ru/catalog/muzhchiny/obuv/filter/size-is-10.5%20uk/apply/?PAGEN_1={page_count}'
        r = s.get(url = url, headers=headers)
        
        data = r.json()    # Спарсили все json из всех страниц сайта, которые нам нужны (выборка сайтов в ссылке) 
        
        products = data.get('products')
        for product in products:
            product_colors = product.get('colors')
            
            for pc in product_colors:
                discount_percent = pc.get('price').get('discountPercent')   # Для того, чтобы все товары были по скидке
                
                if discount_percent != 0 and pc.get('link') not in items_link:
                    items_link.append(pc.get('link'))
                    result.append(
                        {
                            'title' : pc.get('title'),
                            'category' : pc.get('category'),
                            'link' : f"https://salomon.ru{pc.get('link')}",
                            'price' : pc.get('price').get('base'),
                            'sale' : pc.get('price').get('sale'),
                            'discount_percent' : discount_percent
                        }
                    ) 
        
        print(f'{page_count} / {pagination_count}')          
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)    

def main():
    # get_page(url= 'https://salomon.ru/catalog/muzhchiny/obuv/')
    # get_json(url = 'https://salomon.ru/catalog/muzhchiny/obuv/filter/size-is-10.5%20uk/apply/?PAGEN_1=2')
    get_collect()
    
if __name__ == '__main__':
    main()
    
