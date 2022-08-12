from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_load = KeyboardButton('Заказать')
button_delete = KeyboardButton('/Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete)