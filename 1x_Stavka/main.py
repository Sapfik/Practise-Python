import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json 
#                                           =========== ЧИТАЙ КОД СНИЗУ ВВЕРХ=============



def get_message(first_parts):
    result = {}
    id = first_parts["ID"]
    timestamp = first_parts["TIME"]     #first_parts["TIME"]  указывали это в методе ниже
    game_date = datetime.fromtimestamp(timestamp).strftime('%d.%m %H:%M')   #Переделываем время из 16.... в нормальное, человеческое время
    league = first_parts['League']
    team_1 = first_parts['O1']
    team_2 = first_parts['O2']
    total = first_parts['total']
    total_high = first_parts['total_high']
    total_low = first_parts['total_low']
    result[id] = {
        league,
        game_date,
        team_1,
        team_2,
        total,
        total_high,
        total_low
    }
    # message = (f'{league}\n{team_1} VS {team_2}\nТотал: {total}\nТотал меньше: {total_low}\nТотал больше: {total_high}\n{game_date}')
    
    with open('final_result.json', 'a', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
    
    


def get_falls(game_result, game_id):
    for game in game_result['Value']:
        current_id = game['I']
        if current_id == game_id:
            try:
                first_parts = {}
                # time = game['S']
                # end_time = datetime.timestamp(time).strftime('%d.%m %H:%M')
                first_parts['ID'] = current_id
                first_parts['League'] = game['L']    #Получаем название лиги
                first_parts['TEAM 1'] = game['O1']     #Команда номер один
                first_parts['TEAM 2'] = game['O2']     #Команда номер два
                first_parts['TIME'] = game['S']   #Назначенное время матча
                bets = game['SG']                  #Элемент SG - элемент, где содержится вся информация по ставкам матча 
                for item in bets:
                    try:
                        bet = item['TG']        # Получаем название ставок матча
                        
                    except:
                        bet = item['PN']    # Получаем названия ставок матча
                    
                
                    if "1-я Четверть" in bet:     # Проверяем если эта ставка называется '1-я Четверть'
                        for node in item['E']:    #Если да, то находим элемент, который отдает все цифры ставок
                            table_cell = node['T']   # Находим элемент, который отвечает за номер ставки в item['E']
                            
                            
                            if 9 == table_cell:
                                total = node['P']     #Находим в item['E'] тотал матча
                                coef = node['C']      #Находим в item['E'] максимальный коофициент матча
                                first_parts['total'] = total
                                first_parts['total_high'] = coef
                                  
                            if 10 == table_cell:
                                coef = node['C']   #Находим в item['E'] минимальный коофициент матча
                                first_parts['total_low'] = coef  
                        with open('result.json', 'a', encoding='utf-8') as file:
                            json.dump(first_parts, file, indent=4, ensure_ascii=False)   
                        get_message(first_parts)
                print('#' * 20)
            except:
                pass
            
    # with open('result.json', 'w', encoding='utf-8') as file:
    #     json.dump(first_parts, file, indent=4, ensure_ascii=False)
                    



def get_game(result):
    for game in result['Value']:    #Посдле протчтения json находим Value и просматриваем в нем теги
        game_id = game['I']         #В Value находим айди матча
        champs = game['LI']         # Находим номер матча
       
        params = (
        ('sports', '3'),
        ('champs', champs),
        ('count', '50'),
        ('tf', '2200000'),
        ('tz', '3'),
        ('antisports', '188'),
        ('mode', '4'),
        ('subGames', game_id),
        ('country', '2'),
        ('partner', '51'),
        ('getEmpty', 'true'),
    )

        response = requests.get('https://1xstavka.ru/LineFeed/Get1x2_VZip', params=params)
        game_result = response.json()    #Получаем json из сайта
        get_falls(game_result, game_id)       #На каждой карточке переходим в этот метод и парсим уже ставки  



def main():
    url = 'https://1xstavka.ru/line/Basketball/24593-Germany-BBL/'
    champs = url.split('/')[-2].split('-')[0]        #Вытаскиваем 24593 из ссылки выше
    
    params = (
        ('sports', '3'),
        ('champs', champs),
        ('count', '50'),
        ('tf', '2200000'),
        ('tz', '3'),
        ('antisports', '188'),
        ('mode', '4'),
        ('subGames', '346887081'),
        ('country', '2'),
        ('partner', '51'),
        ('getEmpty', 'true'),
    )

    response = requests.get('https://1xstavka.ru/LineFeed/Get1x2_VZip', params=params)
    result = response.json()    #Получаем json из сайта
    
    get_game(result)   #Отсылаем json, который немного исправили (изменили champs), а это номер матча



if __name__ == '__main__':
    main()