from aiogram.dispatcher import Dispatcher
from aiogram import types, executor, Bot
from aiogram.dispatcher.filters import state
from config import TOKEN, user_id
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from selenium import webdriver
import time
from aiogram.dispatcher.filters import Text
from keyboard_button import markup, keyboard
import asyncio

# logging.basicConfig(level = logging.INFO)
# urls_list = ["https://stackoverflow.com", "https://instagram.com", "https://vk.com"]


# def get_data(url):
#     try:
#         driver = webdriver.Chrome(
#             executable_path="/home/cain/PycharmProjects/selenium_python/chromedriver/chromedriver",
#             options=options
#         )
#         # "C:\\users\\selenium_python\\chromedriver\\chromedriver.exe"
#         # r"C:\users\selenium_python\chromedriver\chromedriver.exe"
#         driver.get(url=url)
#         time.sleep(5)
#         driver.get_screenshot_as_file(f"media/{url.split('//')[1]}.png")
#     except Exception as ex:
#         print(ex)
#     finally:
#         driver.close()
#         driver.quit()
#
#
# if __name__ == '__main__':
#     p = Pool(processes=2)
#     p.map(get_data, urls_list)

bot = Bot(token = '2114002558:AAH5ERVa5R1-i6pPcxrQkOYYsjTpoPNPHUw', parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



video_href = ''
video_link = ''  
channel_videos  = ''
id_channel = '@gaobas_ua'
result = []
result_rode = []
result_sea = []
   

async def start():
        global video_href
        video_href = f'https://www.youtube.com/results?search_query=торт&sp=CAISBAgCEAE%253D'    
        
        driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
        
        driver.get(video_href)
        time.sleep(2)
        
        videos_1 = driver.find_elements_by_id('video-title')

        for k in range(len(videos_1)):
            
            try:
                url = videos_1[k].get_attribute('href')
                if url not in result:
                    result.append(url)
                    await bot.send_message('@gaobas_ua',url)
                else:
                    continue
                    
            except:
                continue
        
        
        driver.close()
      
async def start_2():
        global video_link
        video_link = f'https://www.youtube.com/results?search_query=трасса&sp=CAISBAgCEAE%253D'
            
        driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
        
        driver.get(video_link)
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
        
async def start_3():
        global video_link
        video_link = f'https://www.youtube.com/results?search_query=%D0%B4%D0%BE%D1%80%D0%BE%D0%B3%D0%B0+%D0%BD%D0%B0+%D0%BC%D0%BE%D1%80%D0%B5&sp=CAISBAgCEAE%253D'
            
        driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
        
        driver.get(video_link)
        time.sleep(2)
        
        videos = driver.find_elements_by_id('video-title')

        for i in range(len(videos)):
            
            try:
                link = videos[i].get_attribute('href')
                if link not in result_sea:
                    result_sea.append(link)
                    await bot.send_message('@gaobas_ua',link)
                else:
                    continue
                    
            except:
                continue
        
        driver.close()
        
@dp.message_handler(commands='start')
async def end(message:types.Message):
    await bot.send_message(message.chat.id, 'Привет')
    while True:
        await start()
        time.sleep(60)
        await start_2()
        time.sleep(60)
        await start_3()
        time.sleep(60)

              
      
if __name__ == '__main__':
    executor.start_polling(dp , skip_updates=True)