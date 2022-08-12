from config import TOKEN

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types, Bot
import logging
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters import BoundFilter

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

# class MyFilter(BoundFilter):
#     key = 'is_admin'
    
#     def __init__(self, is_admin):
#         self.is_admin = is_admin
        
#     async def check(self, message:types.Message):
#         member = await bot.get_chat_member(message.chat.id, message.from_user.id)     #Получаем статус участника из написанного сообщения участником в какую-то грпуппу
#         return member.is_chat_admin()
    
# dp.filters_factory.bind(MyFilter)

# @dp.message_handler(is_admin = True)
# async def send_message(message:types.Message):
#     await message.answer('Вы тут главный!')
    


async def my_filters(message:types.Message):
    return {'foo' : 'foo', 'bar' : 42}

@dp.message_handler(my_filters)
async def send_message(message:types.Message, bar : int):
    await message.answer(f'bar = {bar}')
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)