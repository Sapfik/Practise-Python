import asyncio
from aiogram import Bot, Dispatcher , executor
from config import BOT_TOKEN

#  Dispatcher - обработчик всех апдейтов 

loop = asyncio.get_event_loop()  #asyncio.get_event_loop() - Если в текущем потоке ОС не установлен текущий цикл событий, поток ОС является основным и set_event_loop () еще не был вызван, asyncio создаст новый цикл событий и установит его как текущий.
bot = Bot(BOT_TOKEN, parse_mode = "HTML") # parse_mode - офрматирует текст
dp = Dispatcher(bot, loop = loop)

if __name__ == "__main__":
    from handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin)    
