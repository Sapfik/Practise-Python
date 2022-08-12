from aiogram import types

cancel_button = 'Отменить'
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(cancel_button)

start_button = ['Все видео', 'Последние 10 видео', 'Видео с канала']
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*start_button)