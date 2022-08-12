from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton
from create_bot import dp, bot
from keyboards import client_kb as nav
from data_base import sqlite_db
import logging

logging.basicConfig(level = logging.INFO)
CHANNEL_ID = '@testchannel1256'  
NOTSUB_MESSAGE = 'Для доступа к функциям бота, подпишитесь на канал!'


def check_sub_members(chat_member):
    print(chat_member['status'])
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler ( commands=['start', 'help'])
async def welcome (message : types.Message):
  try:
    if message.chat.type == 'private':
        if check_sub_members(await bot.get_chat_member(chat_id= CHANNEL_ID, user_id=message.from_user.id)):
        #await bot.get_chat_member() - запрашивает айди юзера и айди чата
            await bot.send_message(message.from_user.id, 'Приятного апетита!', reply_markup=nav.kb_client)
        else:
            await bot.send_message(message.from_user.id, NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)
  except:
    await message.reply(f'{message.from_user.first_name}, все заказы производятся напрямую в чате с ботом! Перейдите по ссылке: \nhttps://t.me/Pizza_Nemo_Bot \nИ сделайте заказ! 🤡')


@dp.message_handler ( commands=['operating_mode', 'Operation_mode'])
@dp.message_handler ( lambda message: 'Режим' in message.text)
@dp.message_handler (lambda message: 'режим' in message.text)
@dp.message_handler ( lambda message: 'Адрес' in message.text)
@dp.message_handler (lambda message: 'адрес' in message.text)
@dp.message_handler (commands=['adress', 'Adress'])
@dp.message_handler (commands=['varients', 'Varients'])
@dp.message_handler(lambda message: 'Вариант' in message.text)
@dp.message_handler(lambda message: 'вариант' in message.text)
@dp.message_handler(lambda message: 'Пример' in message.text)
@dp.message_handler(lambda message: 'пример' in message.text)
@dp.message_handler(commands=['Меню'])
@dp.message_handler(lambda message: 'Меню' in message.text)
@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if check_sub_members(await bot.get_chat_member(chat_id= CHANNEL_ID, user_id=message.from_user.id)):
            if message.text.lower() == 'меню':
                await bot.send_message(message.from_user.id, await sqlite_db.sql_read(message))
            elif message.text.lower()== 'режим работы':
                await bot.send_message (message.from_user.id, 'ПН - ПТ: 10:00 - 23:00  \nCб и Вс : 9:00 - 2:00 🗓')
                await message.delete()
            elif message.text.lower() == 'адрес':
                  await bot.send_message (message.from_user.id, 'Улица: Пушкина 🏘 \nДом: Калатушкина🏠')
                  await message.delete()
            elif message.text.lower() == 'вариант' or message.text.lower() == 'пример':
                chat_id = message.chat.id 
                text = 'Привет, подпишись на канал =)'
                markup = InlineKeyboardMarkup (
                  inline_keyboard=[
                    [
                      InlineKeyboardButton (text = 'Подпишись', url = 'https://www.youtube.com/channel/UCXRAoUWcfu-wRxBy58uD7lA'),
                      InlineKeyboardButton (text = 'Подписан', callback_data = '123')
                    ],
                    [
                      InlineKeyboardButton (text = 'Мой Телеграм', url = 'https://t.me/ILYACHEREMISIN')
                    ]
                  ]
                )
                photo = open("TRUE PIZZA.jpg", 'rb')
                #await bot.send_message (chat_id=chat_id, text = text, reply_markup=markup)
                await bot.send_photo (caption='Пример нашей пиццы', chat_id=chat_id, photo=photo, reply_markup=markup)
                await message.delete()
            else:
                await bot.send_message(message.from_user.id,'Я вас не понимаю, хозяин =(')
        else:
            await bot.send_message(message.from_user.id, NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)


@dp.callback_query_handler(text = 'sub_channel_done')
async def sub_channel_done(callback: types.Message):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if check_sub_members(await bot.get_chat_member(chat_id= CHANNEL_ID, user_id=callback.from_user.id)):
        await bot.send_message(callback.from_user.id, 'Приятного апетита', reply_markup=nav.kb_client)
    else:
        await bot.send_message(callback.from_user.id, NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)



def register_handlers_client (dp:Dispatcher):
    dp.register_message_handler (welcome, commands=['start', 'help'])
    dp.register_message_handler (bot_message, commands=['operating_mode', 'Operation_mode'])
    dp.register_message_handler (bot_message, lambda message: 'Режим' in message.text)
    dp.register_message_handler (bot_message, lambda message: 'режим' in message.text)
    dp.register_message_handler (bot_message, lambda message: 'Адрес' in message.text)
    dp.register_message_handler (bot_message, lambda message: 'адрес' in message.text)
    dp.register_message_handler (bot_message, commands=['adress', 'Adress'])
    dp.register_message_handler (bot_message, commands=['varients', 'Varients'])
    dp.register_message_handler(bot_message,lambda message: 'Вариант' in message.text)
    dp.register_message_handler(bot_message,lambda message: 'вариант' in message.text)
    dp.register_message_handler(bot_message,lambda message: 'Пример' in message.text)
    dp.register_message_handler(bot_message,lambda message: 'пример' in message.text)




