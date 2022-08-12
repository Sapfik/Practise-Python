from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types
from config import TOKEN
from main import main,get_game,get_falls ,get_message
import json 

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    with open('result.json', encoding='utf-8') as file:
        first_pages = json.load(file)
    print(first_pages)    
    # for k, v in sorted(first_pages.items()):
    #     message_go =
    # await message.answer(first)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
