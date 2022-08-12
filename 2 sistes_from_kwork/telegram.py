from  aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types
import json
from config import TOKEN
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.utils.markdown import hbold, hlink


bot = Bot(token = TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(CommandStart())
async def start(message:types.Message):
    start_buttons = ['Все товары', 'Свежие товары']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer('Товары', reply_markup=keyboard)

@dp.message_handler(Text(equals='Все товары'))
async def all_cars(message:types.Message):
    with open('result.json', encoding='utf-8') as file:
        result_dict = json.load(file)
        
    for k, v in sorted(result_dict.items()):
        cars = f"{hlink(v['title'], v['link'])}\n" \
               f"{hbold(v['price'])}\n" \
               f"{hbold(v['mileage'])}\n" \
               f"<i>{v['year']}</i>"
               
        await message.answer(cars)
        
@dp.message_handler(Text(equals='Свежие товары'))
async def fresh_cars(message: types.Message):
    from main import check_data
    fresh_cars = check_data()
    
    if len(fresh_cars) >=1:
        for k, v in sorted(fresh_cars.items()):
            cars = f"{hlink(v['title'], v['link'])}\n" \
               f"{hbold(v['price'])}\n" \
               f"{hbold(v['mileage'])}\n" \
               f"<i>{v['year']}</i>"
            
            await message.answer(cars)
            
    else:
        await message.answer('Пока нету свежих новостей...')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)