from config import weather_token
import requests
from pprint import pprint
import datetime

def get_weather(city, weather_token):
    
    code_to_smile  = {
        "Clear" : "Ясно \U00002600",
        "Clouds" : "Облачно \U00002601",
        "Rain" : 'Дождь \U00002614',
        "Drizzle" : "Дождь \U00002614",
        "Thundertorm" : "Гроза \U000026A1",
        "Snow" : "Снег \U0001F328",
        "Mist" : 'Туман \U0001F32B'
    }
    
    
    
    try:
        r = requests.get(url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric')
        data = r.json()   # Можем читать json, так как парсим данные с сайта, который совместим с Python и дает ему данные из json
        # pprint(data)   # pprint() - так как мы хотим сделать json более структуированным
        
        city = data['name']
        temp = data['main']['temp']
        
        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
            
        else:
            wd = 'Выгляни в окно и сам все увидишь!'
        
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        
        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n" \
              f"Погода в городе: {city}\nТемпература: {temp} °C {wd}\n"\
              f"Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст\n"\
              f"Ветер: {wind} м/с\nВремя восхода: {sunrise_time}\n"\
              f"Время захода: {sunset_time}\nПродолжительность дня: {lenght_of_the_day}\n"\
              f"Хорошего дня!"
              )
        
    except Exception as ex:
        print(ex)
        print('Введите правильное название города!')

def main():
    city = input('Введите название города: ')
    get_weather(city = city, weather_token=weather_token)
    
if __name__ == '__main__':
    main()