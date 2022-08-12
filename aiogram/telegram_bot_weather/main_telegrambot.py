from aiogram.types import message
import requests
import datetime
from config import weather_token, token_bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types

bot = Bot(token = token_bot, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_command (message:types.Message):
    await message.answer("Привет! Напиши мне название города и я пришлю тебе сводку погоды!")
    
@dp.message_handler()
async def get_weather(message:types.Message):
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
        r = requests.get(url = f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric')
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
        
        await message.answer(f"🕐🕐🕐 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} 🕐🕐🕐\n" \
              f"Погода в городе: {city}\nТемпература: {temp} °C {wd}\n"\
              f"Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст\n"\
              f"Ветер: {wind} м/с\nВремя восхода: {sunrise_time}\n"\
              f"Время захода: {sunset_time}\nПродолжительность дня: {lenght_of_the_day}\n"\
              f"🔥🔥🔥 Хорошего дня 🔥🔥🔥"
              )
        
    except :
        await message.reply('Введите более корректное название города')
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)