from fake_useragent import UserAgent
import requests
import json
# Не импортируем BeautifulSoup, так как все будем делать через json

ua = UserAgent()     #Делаем разный user-agent, чтобы сайт нас не блокировал
# print(ua.random)

def collect_data(cat_type = 2):
    # response = requests.get(
    #     url='https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&hasTradeLock=false&hasTradeLock=true&isStore=true&limit=60&maxPrice=10000&minPrice=1&offset=0&tradeLockDays=1&tradeLockDays=2&tradeLockDays=3&tradeLockDays=4&tradeLockDays=5&tradeLockDays=6&tradeLockDays=7&tradeLockDays=0&type=2&withStack=true',
    #     headers= {'user-agent' : f'{ua.random}'}
    #     )
    
    # with open('result.json', 'w', encoding='utf-8') as file:
    #     json.dump(response.json(), file, indent=4, ensure_ascii=False)   #response.json() - записывает json, который на сайте
    
    offset = 0
    batch_size = 60    #Размер партии
    result = []
    count = 0
    while True:
        for item in range(offset, offset + batch_size, 60):    #С шагом на 60
            # url = item
            # print(url)
            req = requests.get(
                url = f'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&hasTradeLock=false&hasTradeLock=true&isStore=true&limit=60&maxPrice=10000&minPrice=2000&offset={item}&tradeLockDays=1&tradeLockDays=2&tradeLockDays=3&tradeLockDays=4&tradeLockDays=5&tradeLockDays=6&tradeLockDays=7&tradeLockDays=0&type={cat_type}&withStack=true',
                headers= {'user-agent' : f'{ua.random}'}
                )
            
            offset += batch_size
            
            data = req.json()     #Просматриваем json на каждой странице
            items = data.get('items')   #Находим в json категорию items
            
            for i in items:
                #Если скидка не равна null и скидка больше 10%
                if i.get('overprice') is not None and i.get('overprice') < -10:
                    item_full_name = i.get('fullName')
                    item_3d = i.get('3d')
                    item_price = i.get('price')
                    item_overprice = i.get('overprice')
                    item_pattern = i.get('pattern')
                    
                    result.append(
                        {
                            'item name' : item_full_name,
                            'item 3d link' : item_3d,
                            'item price' : item_price,
                            'overprice' : item_overprice,
                            'pattern' : item_pattern
                        }
                    )
        
        count += 1
        print(f'Page #{count}')
                    
        if len(items) < 60 :
            break      
        
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)      

    print(len(result))
    
    
def main():
    collect_data()
    
if __name__ == '__main__':
    main()    
    
