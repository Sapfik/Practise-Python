from aiogram.dispatcher import Dispatcher
from aiogram.types import message_auto_delete_timer_changed
from aiogram.utils import executor
from aiogram import types, Bot
import sqlite3
from config import TOKEN
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text 

bot = Bot(token = TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    button = types.KeyboardButton('Получить все данные')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button)
    
    await message.answer('Нажмите на кнопку, чтобы увидеть полный фарш', reply_markup=keyboard)

@dp.message_handler(Text(equals='Получить все данные'))
async def next_func(message:types.Message):
    sql = sqlite3.connect('countries.sqlite')
    cursor = sql.cursor()
    try:
        cursor.execute("""SELECT russion_text,english_text,symbols_text FROM countries""")
        massive = cursor.fetchall()
        for row in massive:
            countries = f"Страна на русском: {hbold(row[0])}\n" \
                        f"Страна на английском: {hbold(row[1])}\n" \
                        f"Индекс страны: {hbold(row[2])}"
            
            await message.answer(countries)
    except:
        pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
