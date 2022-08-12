from aiogram.dispatcher import Dispatcher
from aiogram import executor, Bot, types
from config import TOKEN
import json
from aiogram.dispatcher.filters import Text
from main import get_collect
from aiogram.utils.markdown import hbold, hlink

bot = Bot(token= TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    start_buttons = ['Кроссовки', 'Видосы', 'Сливы']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer('Кроссовки по скидке', reply_markup=keyboard)

@dp.message_handler(Text(equals='Кроссовки'))
async def sneakers(message:types.Message):
    await message.answer('Подождите пару секунд...')
    
    get_collect()
    
    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)
        
    for item in data:
        card = f"{hlink(item.get('title'), item.get('link'))}\n"\
               f"{hbold('Категория: ')} {item.get('category')}\n" \
               f"{hbold('Базовая цена: ')} {item.get('price')}\n"\
               f"{hbold('Цена со скидкой: ')} {item.get('sale')}\n"\
               f"{hbold('Discount: ')} -{item.get('discount_percent')}%🔥"
               
        await message.answer(card)
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)