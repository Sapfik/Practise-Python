from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton
from create_bot import dp, bot
from keyboards import client_kb as nav
from data_base import sqlite_db
import logging


# def check_sub_members(chat_member):
#     print(chat_member['status'])
#     if chat_member['status'] != 'left':
#         return True
#     else:
#         return False



async def welcome (message : types.Message):
  try:
    await bot.send_message(message.from_user.id, 'Приятного апетита', reply_markup=nav.kb_client)
    await message.delete()
      
  except:
    await message.reply(f'{message.from_user.first_name}, все заказы производятся напрямую в чате с ботом! Перейдите по ссылке: \nhttps://t.me/Pizza_Nemo_Bot \nИ сделайте заказ! 🤡')




async def command_operation_mode (message: types.Message):
  
  await bot.send_message (message.from_user.id, 'ПН - ПТ: 10:00 - 23:00  \nCб и Вс : 9:00 - 2:00 🗓')
  await message.delete()



async def command_adress (message:types.Message):
  await bot.send_message (message.from_user.id, 'Улица: Пушкина 🏘 \nДом: Калатушкина🏠')
  await message.delete()


async def send_photo(message:types.Message):
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


@dp.message_handler(commands=['Меню'])
@dp.message_handler(lambda message: 'Меню' in message.text)
async def menu_command(message: types.Message):
  await sqlite_db.sql_read(message)




def register_handlers_client (dp:Dispatcher):
    dp.register_message_handler (welcome, commands=['start', 'help'])
    dp.register_message_handler (command_operation_mode, commands=['operating_mode', 'Operation_mode'])
    dp.register_message_handler (command_operation_mode, lambda message: 'Режим' in message.text)
    dp.register_message_handler (command_operation_mode, lambda message: 'режим' in message.text)
    dp.register_message_handler (command_adress, lambda message: 'Адрес' in message.text)
    dp.register_message_handler (command_adress, lambda message: 'адрес' in message.text)
    dp.register_message_handler (command_adress, commands=['adress', 'Adress'])
    dp.register_message_handler (send_photo, commands=['varients', 'Varients'])
    dp.register_message_handler(send_photo,lambda message: 'Вариант' in message.text)
    dp.register_message_handler(send_photo,lambda message: 'вариант' in message.text)
    dp.register_message_handler(send_photo,lambda message: 'Пример' in message.text)
    dp.register_message_handler(send_photo,lambda message: 'пример' in message.text)
    # dp.register_message_handler(menu_command, commands=['Меню'])
    # dp.register_message_handler(send_photo,lambda message: 'Меню' in message.text)
