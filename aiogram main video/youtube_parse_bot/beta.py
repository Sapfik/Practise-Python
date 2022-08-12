from aiogram.dispatcher import Dispatcher, storage
from aiogram import types, executor, Bot
from config import TOKEN, user_id
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from selenium import webdriver
import time
import asyncio





bot = Bot(token = '2114002558:AAH5ERVa5R1-i6pPcxrQkOYYsjTpoPNPHUw', parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



video = ''  
channel_videos  = ''
id_channel = '@gaobas_ua'
result = []
result_rode = []

class Form(StatesGroup):
    cake = State()
    road = State()
    
@dp.message_handler(commands='start')
async def start(message:types.Message):
    await Form.cake.set()
    await bot.send_message(message.chat.id, 'Привет')


@dp.message_handler(state=Form.cake)
async def cake(message:types.Message, state:FSMContext):
        global video
        await bot.send_message(message.chat.id,'Торты')
        async with state.proxy() as data:
            data['cake'] = 'https://www.youtube.com/results?search_query=торт&sp=CAISBAgCEAE%253D'
            video = data['cake']
            
        driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
        # video_href = f'https://www.youtube.com/results?search_query=торт&sp=CAISBAgCEAE%253D'
        driver.get(video)
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
        await Form.next()

@dp.message_handler(state=Form.road)
async def road(message:types.Message,state:FSMContext):
        global channel_videos
        await bot.send_message(message.chat.id,'Трасса')
        async with state.proxy() as data:
            data['road'] = 'https://www.youtube.com/results?search_query=python&sp=CAISBAgCEAE%253D'
            channel_videos = data['road']
        browser = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
        
        browser.get(channel_videos)
        time.sleep(2)
        
        videos_2 = browser.find_elements_by_id('video-title')

        for i in range(len(videos_2)):
            
            try:
                url = videos_2[i].get_attribute('href')
                if url not in result_rode:
                    result_rode.append(url)
                    await bot.send_message('@gaobas_ua',url)
                else:
                    continue
                    
            except:
                continue
        
        browser.close()
        await state.finish()
        


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)