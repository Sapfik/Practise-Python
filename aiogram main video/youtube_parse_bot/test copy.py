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
from multiprocessing import Pool

# logging.basicConfig(level = logging.INFO)

# storage = MemoryStorage()
bot = Bot(token = '2114002558:AAH5ERVa5R1-i6pPcxrQkOYYsjTpoPNPHUw', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



video = ''  
channel_videos  = ''
id_channel = '@gaobas_ua'
result = []
result_rode = []

# class Form(StatesGroup):
#     search_video = State()

# @dp.message_handler(commands='start')
# async def cmd_start(message:types.Message):
    
#     await message.answer('Выберите команду')
    
    
urls_list = ['https://www.youtube.com/results?search_query=торт&sp=CAISBAgCEAE%253D', 'https://www.youtube.com/results?search_query=трасса&sp=CAISBAgCEAE%253D']  
@dp.message_handler(commands='start')
async def start(url):
    try:
        driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
        driver.get(url=url)
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
    except Exception as ex:
        print(ex)
    
    finally:
        driver.close()
        driver.quit()

if __name__ == '__main__':
    p = Pool(processes=2)
    p.map(start, urls_list)
   
    

# async def start_button():
#     # global id_channnel
#     # global video
#     # await bot.send_message(user_id ,'Начинаю поиск!')
    
#     driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
#     video_href = f'https://www.youtube.com/results?search_query=торт&sp=CAISBAgCEAE%253D'
#     driver.get(video_href)
#     time.sleep(2)
    
#     videos = driver.find_elements_by_id('video-title')

#     for i in range(len(videos)):
        
#         try:
#             link = videos[i].get_attribute('href')
#             if link not in result:
#                 result.append(link)
#                 await bot.send_message('@gaobas_ua',link)
#             else:
#                 continue
                
#         except:
#             continue
    
#     driver.close()
     

# async def start_road():
#     # global id_channnel
#     # global video
#     # await bot.send_message(user_id,'Начинаю поиск!')
    
#     driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
#     video_href = f'https://www.youtube.com/results?search_query=трасса&sp=CAISBAgCEAE%253D'
#     driver.get(video_href)
#     time.sleep(2)
    
#     videos = driver.find_elements_by_id('video-title')

#     for i in range(len(videos)):
        
#         try:
#             link = videos[i].get_attribute('href')
#             if link not in result_rode:
#                 result_rode.append(link)
#                 await bot.send_message('@gaobas_ua',link)
#             else:
#                 continue
                
#         except:
#             continue
    
#     driver.close()
    
# @dp.message_handler() 

# async def start():
#     while True:
#         global id_channnel
#         global video
#         await bot.send_message(user_id,'Начинаю поиск!')
        
#         driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
#         video_href = f'https://www.youtube.com/results?search_query=торт&sp=CAISBAgCEAE%253D'
#         driver.get(video_href)
#         time.sleep(2)
        
#         videos = driver.find_elements_by_id('video-title')

#         for i in range(len(videos)):
            
#             try:
#                 link = videos[i].get_attribute('href')
#                 if link not in result:
#                     result.append(link)
#                     await bot.send_message('@gaobas_ua',link)
#                 else:
#                     continue
                    
#             except:
#                 continue
        
        
#         # driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
#         # video_href = f'https://www.youtube.com/results?search_query=трасса&sp=CAISBAgCEAE%253D'
#         driver.get('https://www.youtube.com/results?search_query=трасса&sp=CAISBAgCEAE%253D')
#         time.sleep(2)
        
#         videos = driver.find_elements_by_id('video-title')

#         for i in range(len(videos)):
            
#             try:
#                 link = videos[i].get_attribute('href')
#                 if link not in result_rode:
#                     result_rode.append(link)
#                     await bot.send_message('@gaobas_ua',link)
#                 else:
#                     continue
                    
#             except:
#                 continue
        
#         driver.close()
#         asyncio.sleep(10)
  
# async def shedule():
    # while True:
    #     global id_channnel
    #     global video
    #     await bot.send_message(user_id,'Начинаю поиск!')
        
    #     driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
    #     video_href = f'https://www.youtube.com/results?search_query=торт&sp=CAISBAgCEAE%253D'
    #     driver.get(video_href)
    #     time.sleep(2)
        
    #     videos = driver.find_elements_by_id('video-title')

    #     for i in range(len(videos)):
            
    #         try:
    #             link = videos[i].get_attribute('href')
    #             if link not in result:
    #                 result.append(link)
    #                 await bot.send_message('@gaobas_ua',link)
    #             else:
    #                 continue
                    
    #         except:
    #             continue
        
    #     driver.close()
        
# async def schedule_road():      
#         driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
#         video_href = f'https://www.youtube.com/results?search_query=трасса&sp=CAISBAgCEAE%253D'
#         driver.get(video_href)
#         time.sleep(2)
        
#         videos = driver.find_elements_by_id('video-title')

#         for i in range(len(videos)):
            
#             try:
#                 link = videos[i].get_attribute('href')
#                 if link not in result_rode:
#                     result_rode.append(link)
#                     await bot.send_message('@gaobas_ua',link)
#                 else:
#                     continue
                    
#             except:
#                 continue
        
#         driver.close()
        
        
        

# async def main():
#     while True:
#         start_button()
#         start_road()
#         await asyncio.sleep(10)
        
        
        
      
