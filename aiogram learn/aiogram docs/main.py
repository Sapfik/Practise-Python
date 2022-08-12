from config import TOKEN

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types, Bot
import logging
from aiogram.dispatcher.filters import Text

logging.basicConfig(level=logging.INFO)    #Настройка журнала

# Иницилизируем бота и диспатчер
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

#По каманде /start or /help бот будет нам овтечать какую-то фразу

@dp.message_handler(commands=['start', 'help'])
async def send_message(message:types.Message):
    await message.reply('Hi!\nI am Echo Bot\nWhat are you wanting?')   #Если мы просто отвечаем
    
@dp.message_handler(commands=['image', 'img'])
async def send_photo(message:types.Message):
    url = 'https://docs.aiogram.dev/en/latest/_static/logo.png'
    await bot.send_photo(message.chat.id, types.InputFile.from_url(url))
    
@dp.message_handler(Text(contains='spam'))
async def text_contain(message:types.Message):
    await message.answer('You have in text spam')


    
@dp.message_handler()
async def echo_text(message:types.Message):
    await message.reply(message.text)     #Если повторяем за пользователем      
    
    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    

