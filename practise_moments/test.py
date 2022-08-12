import os
from aiogram import Bot, types
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text



bot = Bot(token = '2028825065:AAGSya1ClSfmPDDBywhidDuQ7roYQESz0Lg')
dp = Dispatcher(bot)
answer = dict()

#Кнопка и ссылка 
urlkb = InlineKeyboardMarkup(row_width=1)
url1 = InlineKeyboardButton(text = 'Youtube', url='https://www.youtube.com/watch?v=gpCIfQUbYlY&t=7s&ab_channel=PythonHubStudio')
url2 = InlineKeyboardButton(text = 'Seasonvar', url= 'http://seasonvar.ru/serial-13996-Flesh--000003-sezon.html')
markup = [InlineKeyboardButton(text = 'Youtube', url = 'https://www.youtube.com/watch?v=gpCIfQUbYlY&t=7s&ab_channel=PythonHubStudio'), InlineKeyboardButton(text = 'Youtube', url='https://www.youtube.com/watch?v=gpCIfQUbYlY&t=7s&ab_channel=PythonHubStudio'), InlineKeyboardButton(text = 'Youtube', callback_data = '123'),]
urlkb.add(url1, url2).row(*markup).insert(InlineKeyboardButton(text = 'Youtube', url='https://www.youtube.com/watch?v=gpCIfQUbYlY&t=7s&ab_channel=PythonHubStudio'))


@dp.message_handler(commands = ['links'])
async def links(message:types.Message):
    await message.answer('Ссылки на полезные сайты', reply_markup=urlkb)


markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text = 'Like', callback_data='like_1'),\
                                               InlineKeyboardButton(text = 'Dislike', callback_data='like_-1'))

@dp.message_handler(commands=['test'])
async def test (message:types.Message):
    await message.answer ('Инлайн кнопка', reply_markup=markup)



@dp.callback_query_handler(Text(startswith='like_'))
async def vote (callback:CallbackQuery):
    res = int(callback.data.split('_')[1])
    if f'{callback.from_user.id}' not in answer:
        answer[f'{callback.from_user.id}'] = res
        await callback.answer('Вы проголосовали!')
    else:
        await callback.answer('Вы уже проголосовали!', show_alert=True)
    #show_alert - выбивает предупредительное окно
executor.start_polling(dp, skip_updates=True)

