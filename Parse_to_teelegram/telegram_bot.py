import asyncio
from aiogram import Dispatcher, types, executor, Bot
from config import token, user_id
from aiogram.utils.markdown import hbold, hcode, hlink, hunderline
import json
import datetime
from main import check_news_update
from aiogram.dispatcher.filters import Text

bot = Bot(token = token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    start_buttons = ['Все новости', 'Последние 5', 'Свежие новости']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Лента новостей', reply_markup=keyboard)

@dp.message_handler(Text(equals='Все новости'))
async def get_all_news (message: types.Message):
    with open ('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)
    
    for k, v in sorted(news_dict.items()):
        # news = f"<b>{datetime.datetime.fromtimestamp(v['article_date_time_step'])}</b>\n" \
        #        f"<u>{v['article title']}</u>\n" \
        #        f"<code>{v['article description']}</code>\n" \
        #        f"{v['article link']}"

        # news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_time_step']))}\n" \
        # f"{hunderline(v['article title'])}\n" \
        # f"{hcode(v['article description'])}\n" \
        # f"{hlink(v['article title'], v['article link'])}"

        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_time_step']))}\n" \
        f"{hlink(v['article title'], v['article link'])}"

        await message.answer(news)


@dp.message_handler(Text(equals='Последние 5'))
async def get_last_five_news(message:types.Message):
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_time_step']))}\n" \
        f"{hlink(v['article title'], v['article link'])}"

        await message.answer(news)


@dp.message_handler(Text(equals='Свежие новости'))
async def get_fresh_news (message:types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_time_step']))}\n" \
            f"{hlink(v['article title'], v['article link'])}"

            await message.answer(news)
    else:
        await message.answer('Пока что нету свежих новостей...')

async def news_every_half_an_hour():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_time_step']))}\n" \
                f"{hlink(v['article title'], v['article link'])}"

                await bot.send_message(user_id,news, disable_notification=True)
        else:
            await bot.send_message(user_id, 'Пока нет свежих новостей', disable_notification=True)

        await asyncio.sleep(1800)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_half_an_hour())
    executor.start_polling(dp, skip_updates=True)   