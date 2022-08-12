from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
# import markups as nav

TOKEN = '5524891851:AAER4AnQN4pleTXAF3iZBsKbEAg-k18VaE8'
CHANNEL_ID = '-1001799237581'
NOTSUB_MESSAGE = 'Для доступа к функционалу бота, подпишитесь на канал!'


bot = Bot(token = TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False
    

@dp.message_handler(commands=['start'])    
async def start(message: types.Message):
    if message.chat.type == 'private':
        if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):   
            await message.reply('Привет!')
        else:
            await bot.send_message(message.from_user.id, NOTSUB_MESSAGE)
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)