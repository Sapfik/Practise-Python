from contextvars import Token
import config 
import logging

from filters import IsAdminFilter

import json, string
from aiogram import Bot, executor, Dispatcher, types

#log level 
logging.basicConfig(level = logging.INFO)

bot = Bot(token = config.TOKEN)
dp = Dispatcher(bot)

#@dp.message_handler()
dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(content_types=['new_chat_members'])
async def joined_member (message:types.Message):
    await message.delete()


@dp.message_handler(is_admin = True, commands=['ban'], commands_prefix = "!/")
async def ban_command(message: types.Message):
    if not message.reply_to_message:
        await message.reply ('Чтобы забанить человека,вы должны ответить на его сообщение')
        return 
    await message.bot.delete_message(chat_id = config.GROUP_ID, message_id = message.message_id)
    await message.bot.kick_chat_member (chat_id = config.GROUP_ID, user_id = message.reply_to_message.from_user.id)

    await message.reply_to_message.reply('Правосудие свершилось, равновесие восстановлено \nЯ единственный вершитель правосудия')

@dp.message_handler()
async def echo (message :types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
    .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('маты запрещенны у данного Telegram бота') 
        await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

