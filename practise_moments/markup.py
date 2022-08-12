from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

profile_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('ПРОФИЛЬ'))  

btn_url_button = InlineKeyboardButton(text = 'ПОДПИСАТЬСЯ', url = 'https://t.me/testchannel1256')
btn_done = InlineKeyboardButton(text = 'ПОДПИСАЛСЯ', callback_data='sub_channel_done')

checkSubMenu = InlineKeyboardMarkup(row_width=1)
checkSubMenu.insert(btn_url_button).insert(btn_done)   