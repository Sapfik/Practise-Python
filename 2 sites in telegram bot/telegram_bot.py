from aiogram.dispatcher import Dispatcher
from aiogram import executor, types, Bot
from aiogram.dispatcher.filters import Text
from main import check_news, check_news_hi_tech
from config import TOKEN, user_id
import json
from aiogram.utils.markdown import hbold, hcode, hlink
import datetime

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start (message:types.Message):
    start_buttons = ['Все новости', 'Последние 10', 'Свежие новости']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer('Новости', reply_markup=keyboard)
  
  
@dp.message_handler(Text(equals='Все новости'))
async def all_news (message:types.Message):
    with open('news_dict.json',encoding='utf-8') as file:
        news_dict = json.load(file)
        
    for k,v in sorted(news_dict.items()):
        # news = f"{datetime.datetime.fromtimestamp(v['Date Time'])}\n{v['Title']}\n{v['Card description']}\n{v['Link']}"
        # await message.answer(news)
        
        news = f"{hbold(datetime.datetime.fromtimestamp(v['Date Time']))}\n{hlink(v['Title'], v['Link'])}"
        await message.answer(news)
        
        
    with open('article_dict.json', encoding='utf-8') as file:
        article_dict = json.load(file)
        
    for k, v in sorted(article_dict.items()):
        news = f"{hbold(v['Date time'])}\n{hlink(v['Title'], v['Link'])}"
        await message.answer(news)
       
        

@dp.message_handler(Text(equals='Последние 10'))     
async def last_five(message:types.Message):
    with open('news_dict.json',encoding='utf-8') as file:
        news_dict = json.load(file)
        
    for k,v in sorted(news_dict.items())[-5:]: 
        news = f"{hbold(datetime.datetime.fromtimestamp(v['Date Time']))}\n{hlink(v['Title'], v['Link'])}"
        await message.answer(news)
        
    with open('article_dict.json', encoding='utf-8') as file:
        article_dict = json.load(file)
        
    for k, v in sorted(article_dict.items())[-5:]:
        news = f"{hbold(v['Date time'])}\n{hlink(v['Title'], v['Link'])}"
        await message.answer(news)
        
       
@dp.message_handler(Text(equals='Свежие новости'))
async def fresh_news(message:types.Message):
    fresh_news = check_news()
    
    if len(fresh_news) >= 1:
        for k,v in sorted(fresh_news.items()):
            news = f"{hbold(datetime.datetime.fromtimestamp(v['Date Time']))}\n{hlink(v['Title'], v['Link'])}"
            await message.answer(news)
        
         
    fresh_news_hi_tech = check_news_hi_tech()
    if len(fresh_news_hi_tech) >= 1:
        for k, v in sorted(fresh_news_hi_tech.items()):
            news = f"{hbold(v['Date time'])}\n{hlink(v['Title'], v['Link'])}"
            await message.answer(news)
            
    if len(fresh_news_hi_tech) < 1 and len(fresh_news) < 1:
        await message.answer('Пока что нету свежых новостей...')
  
  
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)