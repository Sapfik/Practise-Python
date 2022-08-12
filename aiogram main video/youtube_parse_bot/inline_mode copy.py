from aiogram.dispatcher import Dispatcher
from aiogram import types, executor, Bot
from aiogram.dispatcher.filters import state
from config import TOKEN
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from selenium import webdriver
import time
from aiogram.dispatcher.filters import Text
from keyboard_button import markup, keyboard

logging.basicConfig(level = logging.INFO)


bot = Bot(token = TOKEN, parse_mode=types.ParseMode.HTML)
storage  = MemoryStorage()
dp = Dispatcher(bot, storage = storage)


class Form(StatesGroup):
    search_video = State()
    # searching  = State()

video = ''  
channel_videos  = ''
id_channel = "@gaobas_ua"


@dp.message_handler(commands='start')
async def cmd_start(message:types.Message):
    
    await message.answer('Выбери кнопку!', reply_markup=keyboard)
    
    
@dp.message_handler(Text(equals='Все видео'))
async def start_button(message:types.Message):
    await Form.search_video.set()
    await message.answer("Теперь напиши что хочешь получить 🐍", reply_markup=markup)
    
@dp.message_handler(Text(equals='Отменить', ignore_case=True), state='*')
async def cancel_all_videos (message:types.Message, state:FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    
    await message.reply('Состояние было отменено', reply_markup=keyboard)    

    
@dp.message_handler(state = Form.search_video)
async def process_search_video (message:types.Message, state: FSMContext):
    global video
    await message.answer(f'Начинаю поиск', reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as data:
        data['search_video'] = message.text
        video = data['search_video']
    
    driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
    video_href = f'https://www.youtube.com/results?search_query={video}'
    driver.get(video_href)
    time.sleep(2)
    
    videos = driver.find_elements_by_id('video-title')
    
    for i in range(len(videos)):
        try:
            await bot.send_message(id_channel, videos[i].get_attribute('href'), reply_markup=keyboard)
        except:
            continue
    
    driver.close()
    
    await state.finish()
    

class FSMten(StatesGroup):
    search_last_ten_videos = State()
    
@dp.message_handler(Text(equals='Последние 10 видео'))
async def start_button(message:types.Message):
    
    await FSMten.search_last_ten_videos.set()
    await message.answer("Теперь напиши что хочешь получить 🐍")
    
@dp.message_handler(state = FSMten.search_last_ten_videos)
async def process_search_video (message:types.Message, state: FSMContext):
    global video
    await message.answer(f'Начинаю поиск')
    async with state.proxy() as data:
        data['search_last_ten_videos'] = message.text
        video = data['search_last_ten_videos']
    
    driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
    video_href = f'https://www.youtube.com/results?search_query={video}'
    driver.get(video_href)
    time.sleep(2)
    
    result = []
    videos = driver.find_elements_by_id('video-title')
    for i in range(len(videos)):
        try:
            if len(result) < 10:
                link = videos[i].get_attribute('href')
                if link is not None:
                    result.append(link)
                await bot.send_message(id_channel, link)
            # if i == 10:
            #     break
    
        except:
            continue
        
    driver.close()
    
    await state.finish()    
    
    
class FSMChannel (StatesGroup):
    channel = State()
    
@dp.message_handler(Text(equals='Видео с канала'))
async def  channel(message:types.Message):
    await FSMChannel.channel.set()
    await message.answer('Введите ссылку на YouTube канал, который хотите найти 🎞')
    
@dp.message_handler(state = FSMChannel.channel)
async def search_channel(message:types.Message, state: FSMChannel):
    global channel_videos
    await message.answer('Начинаю поиск')
    async with state.proxy() as data:
        data['channel'] = message.text
        channel_videos = data['channel']
    try:   
        driver = webdriver.Chrome(executable_path=r'D:\Practise Python\aiogram main video\chromedriver.exe')
        video_links = f'{channel_videos}/videos'
        driver.get(video_links)
        time.sleep(2)   
    except Exception as ex:
        print(ex)
    
    videos_cards = driver.find_elements_by_id('video-title')
    for card in range(len(videos_cards)):
        try:
            await bot.send_message(id_channel, videos_cards[card].get_attribute('href'))
        except:
            continue
        
    driver.close()
    
    await state.finish()
        

# /html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[2]/div[3]/ytd-playlist-renderer[1]/div/a
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)