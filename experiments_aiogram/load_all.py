import asyncio
import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from language_middleware import setup_middleware   # Функция, которая задает обновленный Dispatcher и возвращает видоизмененный i18n

logging.basicConfig(level = logging.INFO)

loop = asyncio.get_event_loop()

storage = MemoryStorage()

bot  = Bot(token = TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

# Настроим i18n middleware для работы с многоязычностью

i18n = setup_middleware(dp)

# Создадим псевдоним для метода gettext
# Функция gettext нужна для того, чтобы когда нам нужно получить текст с нужным переводом, эта функция переводила его

_ = i18n.gettext

