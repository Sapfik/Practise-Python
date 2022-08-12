from aiogram.dispatcher import Dispatcher
from aiogram import types, executor, Bot
from aiogram.dispatcher.filters import state
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from selenium import webdriver
import time
from aiogram.dispatcher.filters import Text
import asyncio

logging.basicConfig(level = logging.INFO)

bot = Bot(token = '2114002558:AAH5ERVa5R1-i6pPcxrQkOYYsjTpoPNPHUw', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



video = ''  
channel_videos  = ''
id_channel = '@gaobas_ua'
result = []
result_rode = []

class Form(StatesGroup):
    search_video = State()

@dp.message_handler(commands='start')
async def cmd_start(message:types.Message):
    
    await message.answer('Выберите команду')
    
    
    
@dp.message_handler(commands='cake')
async def start_button(message:types.Message):
    global id_channnel
    global video
    await message.answer('Начинаю поиск!')
    
    driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
    video_href = f'https://www.youtube.com/results?search_query=торт&sp=CAISBAgCEAE%253D'
    driver.get(video_href)
    time.sleep(2)
    
    videos = driver.find_elements_by_id('video-title')

    for i in range(len(videos)):
        
        try:
            link = videos[i].get_attribute('href')
            if link not in result:
                result.append(link)
                await bot.send_message('@gaobas_ua',link)
            else:
                continue
                
        except:
            continue
    
    driver.close()
    
   
    
  
@dp.message_handler(commands='road')
async def start_button(message:types.Message, state:FSMContext):
    global id_channnel
    global video
    await message.answer('Начинаю поиск!')
    
    driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
    video_href = f'https://www.youtube.com/results?search_query=трасса&sp=CAISBAgCEAE%253D'
    driver.get(video_href)
    time.sleep(2)
    
    videos = driver.find_elements_by_id('video-title')

    for i in range(len(videos)):
        
        try:
            link = videos[i].get_attribute('href')
            if link not in result_rode:
                result_rode.append(link)
                await bot.send_message('@gaobas_ua',link)
            else:
                continue
                
        except:
            continue
    
    driver.close()
    
    asyncio.sleep(10)  
    
    
if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.create_task(start_button())
    executor.start_polling(dp , skip_updates=True)