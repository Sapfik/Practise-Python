from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types
from config import TOKEN
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.utils.markdown import hbold, hlink
from main import collect_data
import json
import time


bot = Bot(token = TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(CommandStart())
async def start(message:types.Message):
    start_buttons = ['🔪 Ножи', '🥊 Перчатки', '🔫 Снайперские винтовки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer('Выберите категорию!', reply_markup=keyboard)
    
@dp.message_handler(Text(equals='🔪 Ножи'))
async def get_discount_knives (message:types.Message):
    await message.answer('Please waiting...')
    
    collect_data(cat_type=2)
    
    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

    for index,item in enumerate(data):
        card = f"{hlink(item.get('item name'), item.get('item 3d link'))}\n" \
            f"{hbold('Скидка: ')}{item.get('overprice')} %\n" \
            f"{hbold('Цена: ')}{item.get('item price')} 🔥\n" \
            f"{hbold('Патерн: ')}{item.get('pattern')}"
        
        if index % 20 == 0:   #Если отослалось 20 сообщений, то мы засыпаем на 3 секунды
            time.sleep(3)    
            
        await message.answer(card)
        
        
@dp.message_handler(Text(equals='🔫 Снайперские винтовки'))
async def get_discount_knives (message:types.Message):
    await message.answer('Please waiting...')
    
    collect_data(cat_type=4)
    
    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

    for index,item in enumerate(data):
        card = f"{hlink(item.get('item name'), item.get('item 3d link'))}\n" \
            f"{hbold('Скидка: ')}{item.get('overprice')} %\n" \
            f"{hbold('Цена: ')}{item.get('item price')} 🔥\n" \
            f"{hbold('Патерн: ')}{item.get('pattern')}"
            
        if index % 20 == 0:   #Если отослалось 20 сообщений, то мы засыпаем на 3 секунды
            time.sleep(3)    
            
        await message.answer(card)
        
        
@dp.message_handler(Text(equals='🥊 Перчатки'))
async def get_discount_knives (message:types.Message):
    await message.answer('Please waiting...')
    
    collect_data(cat_type=13)
    
    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

    for index,item in enumerate(data):
        card = f"{hlink(item.get('item name'), item.get('item 3d link'))}\n" \
            f"{hbold('Скидка: ')}{item.get('overprice')} %\n" \
            f"{hbold('Цена: ')}{item.get('item price')} 🔥\n" \
            f"{hbold('Патерн: ')}{item.get('pattern')}"
            
        if index % 20 == 0:   #Если отослалось 20 сообщений, то мы засыпаем на 3 секунды
            time.sleep(3)    
            
        await message.answer(card)
                    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)