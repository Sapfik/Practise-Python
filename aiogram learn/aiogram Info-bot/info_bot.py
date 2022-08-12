from config import OWM_KEY, TOKEN
import pyowm
import pyowm.commons.exceptions
import time     
from googletrans import Translator
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import hlink, hbold
from uti.news import get_articles
from uti.weather import get_forecast
from uti.world_time import get_time
from uti.translater import *
from uti.crypto_coins import *
from uti.stocks import *

    
bot = Bot(token = TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
owm = pyowm.OWM(OWM_KEY)
trans = Translator()

    
@dp.message_handler(Text(equals=['Start', 'start']))
@dp.message_handler(commands='start')
async def command_start(message:types.Message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.row('Start', 'Help', 'Hide keyboard')
    start_markup.row('Weather', 'Time', 'News')
    start_markup.row('Crypto', 'Stocks', 'Translate')
    
    await bot.send_message(message.chat.id, '🤖 The bot has started!\n⚙ Enter /help or Help to see bot`s functions"')
    await bot.send_message(message.from_user.id, "⌨️ The Keyboard is added!\n⌨️ /hide or 'Hide keyboard' To remove kb", reply_markup=start_markup)


@dp.message_handler(Text(equals='Hide keyboard'))
@dp.message_handler(commands='hide')
async def hide_kb(message:types.Message):
    hide_kb = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, '⌨💤...', reply_markup=hide_kb)
    
@dp.message_handler(Text(equals='Help'))
@dp.message_handler(commands='help')
async def command_help(message:types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "🤖 /start - display the keyboard\n"
									  "☁ /weather - current forecast\n"
									  "💎 /crypto - current cryptocurrency\n"
									  "⌛️ /time - current time\n"
									  "📊 /stocks - current stocks prices\n"
									  "📰 /news - latest bbc article\n"
									  "🔁 /translate - language translator")
    
class Weather(StatesGroup):
    w = State()   
    
class Time(StatesGroup):
    time = State()
@dp.message_handler(commands='weather', state=None)
@dp.message_handler(Text(equals=['Weather', 'weather']), state=None)
async def command_weather(message:types.Message):
    await Weather.w.set()
    await bot.send_message(message.from_user.id, "🗺 Enter the City or Country\n🔍 In such format:  'Moscow'  or  'Kiev'")


 
@dp.message_handler(state = Weather.w)
async def next_weather(message:types.Message, state: FSMContext):
    try:
        forecast = get_forecast(message.text)
        await bot.send_message(message.chat.id, forecast)
        await state.finish()
    except :
        await bot.send_message(message.chat.id, '❌  Wrong place, check mistakes and try again!')
        await state.finish()
        

@dp.message_handler(commands='time')
@dp.message_handler(Text(equals=['Time', 'time']))
async def commansd_time(message:types.Message):
    await Time.time.set()
    await bot.send_message(message.chat.id, "🗺 Enter the City or Country\n🔍 In such format:  'Moscow'  or  'Kiev'")   
    
@dp.message_handler(state=Time.time)
async def next_time(message:types.Message, state: FSMContext):
    try:
        time = get_time(message.text)
        await bot.send_message(message.from_user.id, time)
        await state.finish()
    except:
        await bot.send_message(message.chat.id, '❌  Wrong place, check mistakes and try again!')
        await state.finish()
    

@dp.message_handler(commands='news')
@dp.message_handler(Text(equals=['News', 'news']))
async def command_news(message:types.Message):
    articles = get_articles()
    if len(articles) == 0:
        await bot.send_message(message.chat.id, 'Пока что нету свежих новостей!')
    for k, v in sorted(articles.items()):
        article = f"{hlink(v['Title'], v['Link'])}\n" \
                  f"{hbold(v['Description'])}\n" \
                  f"{hbold(v ['Categorie'])}\n" \
                  f"{hbold(v['Datetime'])}"
                  
        await bot.send_message(message.chat.id, article)
    
@dp.message_handler(commands='crypto')
@dp.message_handler(Text(equals=['Crypto', 'crypto']))
async def command_crypto(message:types.Message):
    coins_markup = types.InlineKeyboardMarkup(row_width=1)
    for key, value in coins.items():    #Это coins из crypto_coins.py
        coins_markup.add(types.InlineKeyboardButton(text=key, callback_data=value))

    await bot.send_message(message.chat.id, "📃 Choose the coin:", reply_markup=coins_markup)

@dp.message_handler(commands='stocks')
@dp.message_handler(Text(equals=['stocks', 'Stocks']))
async def command_stocks(message:types.Message):
    stocks_markup = types.InlineKeyboardMarkup(row_width=1)
    for key, value in stocks.items():
        stocks_markup.add(types.InlineKeyboardButton(text = key, callback_data=value))

    await bot.send_message(message.chat.id, "📃 Choose the company:", reply_markup=stocks_markup)
@dp.callback_query_handler()
async def callback_crypto_stocks(call:types.CallbackQuery):
	if call.message:
		coins_switcher = {
			'BTC': f"💰Bitcoin:  ${btc_price}",
			'ETH': f"💰Ethereum:  ${eth_price}",
            'ATOM' : f"💰Atom:  ${atom_price}",
            'SOL': f"💰Solana:  ${solana_price}",
			'XMR' : f"💰Monero:  ${xmr_price}"
		}
		stocks_switcher = {
            'FB': f"📊Facebook:  {fb_price}",
            'TSLA': f"📊Tesla:  {tsla_price}",
			'GOOG': f"📊Google:  {goog_price}",
			'APL': f"📊Apple:  {appl_price}",
			'NVDA': f"📊NVIDIA:  {nvdia_price}",
		}

		coin_response = coins_switcher.get(call.data)
		if coin_response:
			await bot.send_message(call.message.chat.id, coin_response)
		stock_response = stocks_switcher.get(call.data)
		if stock_response:
			await bot.send_message(call.message.chat.id, stock_response)

class Translate(StatesGroup):
    take_lang = State()


@dp.message_handler(commands='translate')
@dp.message_handler(Text(equals=['translate', 'Translate']))
async def command_translate(message:types.Message):
    trans_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    trans_markup.row('German', 'French', 'Spanish')
    trans_markup.row('Russian', 'Japanese', 'Polish')
    await bot.send_message(message.chat.id, "📃 Choose the language translate to", reply_markup=trans_markup)
    await Translate.take_lang.set()

@dp.message_handler(state=Translate.take_lang)
async def get_input(message:types.Message, state: FSMContext):
    if not any(message.text in item for item in languages):
        hide_markup = types.ReplyKeyboardRemove()
        await bot.send_message(message.chat.id, "❌ Wrong language, choose from butons only", reply_markup=hide_markup)
    else:
        sent = await bot.send_message(message.chat.id, "🚩 Your language is " + message.text + "\n➡️ Enter the input")
        languages_switcher = {
            'Russian': send_rus_trans,
            'German': send_ger_trans,
            'Japanese': send_jap_trans,
            'Polish': send_pol_trans,
            'Spanish': send_spa_trans,
            'French': send_fra_trans
        }

        lang_response = languages_switcher.get(message.text)
        await bot.send_message(message.chat.id , sent, lang_response)

    await state.finish()


async def send_rus_trans(message:types.Message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)  # Return to start keyboard
    start_markup.row('/start', '/help', '/hide')
    start_markup.row('/weather', '/world_time', '/news')
    start_markup.row('/crypto', '/stocks', '/translate')
    await bot.send_message(message.chat.id, to_ru(message.text), reply_markup=start_markup)


async def send_ger_trans(message:types.Message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/start', '/help', '/hide')
    start_markup.row('/weather', '/world_time', '/news')
    start_markup.row('/crypto', '/stocks', '/translate')
    await bot.send_message(message.chat.id, to_de(message.text), reply_markup=start_markup)


async def send_jap_trans(message:types.Message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/start', '/help', '/hide')
    start_markup.row('/weather', '/world_time', '/news')
    start_markup.row('/crypto', '/stocks', '/translate')
    await bot.send_message(message.chat.id, to_ja(message.text), reply_markup=start_markup)


async def send_pol_trans(message:types.Message):
    start_markup =types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/start', '/help', '/hide')
    start_markup.row('/weather', '/world_time', '/news')
    start_markup.row('/crypto', '/stocks', '/translate')
    await bot.send_message(message.chat.id, to_pl(message.text), reply_markup=start_markup)


async def send_spa_trans(message:types.Message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/start', '/help', '/hide')
    start_markup.row('/weather', '/world_time', '/news')
    start_markup.row('/crypto', '/stocks', '/translate')
    await bot.send_message(message.chat.id, to_es(message.text), reply_markup=start_markup)


async def send_fra_trans(message:types.Message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/start', '/help', '/hide')
    start_markup.row('/weather', '/world_time', '/news')
    start_markup.row('/crypto', '/stocks', '/translate')
    await bot.send_message(message.chat.id, to_fr(message.text), reply_markup=start_markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True) 