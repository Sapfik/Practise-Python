from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types
from config import TOKEN
from bs4 import BeautifulSoup
import requests
from selenium  import webdriver
import time


bot = Bot(token = TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# headers = {
#     'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
#     'accept':'*/*'
# }

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await bot.send_message(message.chat.id, """
    Привет! Я бот, который поможет тебе найти быстро и качественно какую-либо вещь <b><a href = 'https://prom.ua/'>PROM.UA</a></b>\n\nДля того, чтобы я отправил вам ответ, введите пожалуйста название категории...""",
    disable_web_page_preview = 1
    ) 
    
@dp.message_handler(content_types='text')    
async def parse_items(message:types.Message):
    links = []
    url = 'https://prom.ua/search?search_term=' + message.text
    req =  requests.get(url=url)
    soup = BeautifulSoup(req.text, 'lxml')
    cards = soup.find_all('div', class_ = '_1KcTA nN6NX _1sZ22 FpIl2 ggTpW _3-zi4 _2hSrY _3bt5s')
    for card in cards:
        url = 'https://prom.ua' + card.find('a', class_ = '_2KaCs xuuH_').get('href')
        links.append(url)
        
    for link in links:
        req = requests.get(link)
        soup = BeautifulSoup(req.text, 'lxml')
        title = soup.find('h1', class_ = '_3h93n _2hJ1M _28iXq _21mbo').text.strip()
        price = soup.find('span', class_ = '_3h93n _2Wxbt').text.strip()
        
        await bot.send_message(message.chat.id,
        f"""<b>{title}</b>\n{price}\n<a href = '{link}'>Ссылка на предмет</a>""")  

    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)