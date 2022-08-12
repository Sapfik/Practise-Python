import logging
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import markup as nav

TOKEN = '2028825065:AAGSya1ClSfmPDDBywhidDuQ7roYQESz0Lg'
CHANNEL_ID = '@testchannel1256'  
NOTSUB_MESSAGE = 'Для доступа к функциям бота, подпишитесь на канал!'
logging.basicConfig(level = logging.INFO)

bot  = Bot(TOKEN)
dp = Dispatcher(bot)


def check_sub_members(chat_member):
    print(chat_member['status'])
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    if message.chat.type == 'private':
        if check_sub_members(await bot.get_chat_member(chat_id= CHANNEL_ID, user_id=message.from_user.id)):
        #await bot.get_chat_member() - запрашивает айди юзера и айди чата
            await bot.send_message(message.from_user.id, 'Привет', reply_markup=nav.profile_btn)
        else:
            await bot.send_message(message.from_user.id, NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if check_sub_members(await bot.get_chat_member(chat_id= CHANNEL_ID, user_id=message.from_user.id)):
            if message.text == 'ПРОФИЛЬ':
                await bot.send_message(message.from_user.id, 'Тут есть какая-то информация')
            else:
                await bot.send_message(message.from_user.id,'Я вас не понимаю, хозяин =(')
        else:
            await bot.send_message(message.from_user.id, NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)
            
@dp.callback_query_handler(text = 'sub_channel_done')
async def sub_channel_done(callback: types.Message):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if check_sub_members(await bot.get_chat_member(chat_id= CHANNEL_ID, user_id=callback.from_user.id)):
        await bot.send_message(callback.from_user.id, 'Привет', reply_markup=nav.profile_btn)
    else:
        await bot.send_message(callback.from_user.id, NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)



executor.start_polling(dp, skip_updates=True)
