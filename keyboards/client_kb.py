from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

b1 = KeyboardButton ('Режим работы')
b2 = KeyboardButton('Адрес')
b3 = KeyboardButton('Меню')
b4 = KeyboardButton ('Вариант')
b5 = KeyboardButton ('Поделится номером телефона', request_contact=True)
b6 = KeyboardButton('Показать совё месторасположение', request_location=True)

#request_contact - запрашивает разрешение на получение телеонных данных от пользывателя 
#request_location - запрашивает месторасположение пользователя

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#one_timeu_keyboard = True - сворачивает клавиатуру после нажатия на одну кнопку

kb_client.add(b1).add(b2).insert(b3).add(b4).row(b5,b6)
#insert() - для добавления кнопки в более читаемое место
#row() - записывает все кнопки в одну строку

btn_url_button = InlineKeyboardButton(text = 'ПОДПИСАТЬСЯ', url = 'https://t.me/testchannel1256')
btn_done = InlineKeyboardButton(text = 'ПОДПИСАЛСЯ', callback_data='sub_channel_done')

checkSubMenu = InlineKeyboardMarkup(row_width=1)
checkSubMenu.insert(btn_url_button).insert(btn_done)