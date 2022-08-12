from aiogram import types
import json,string
from aiogram.dispatcher.dispatcher import Dispatcher

from create_bot import dp 
#@dp.message_handler()
async def cenz(message : types.Message):  #async - нужен для того, чтобы бот быстрее работал 
  if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
    .intersection(set(json.load(open('cenzur.json')))) != set():
    await message.reply('маты запрещенны у данного Telegram бота') 
    await message.delete()

def register_handlers_other (dp:Dispatcher):
    dp.register_message_handler(cenz)