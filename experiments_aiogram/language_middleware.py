from aiogram.contrib.middlewares.i18n import I18nMiddleware
from typing import Tuple, Any
from aiogram import types

from config import I18N_DOMAIN, LOCALES_DIR
# I18nMiddleware - для перевода текста на разные языки



async def get_lang(user_id):
    from datebase import DBCommands

    db = DBCommands()
    user = await db.get_user(user_id)   #Получаем айди пользователя
    if user:     #Если есть такой пользователь, то мы возвращаем язык 
        return user.language   
    return None

# Middleware - связующее программное обеспечение, которое помогает приложению и серверу обмениваться друг с другом запросами.

class ACLMiddleware (I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user = types.User.get_current()    #Получает текущие данные пользователя
        return await get_lang(user.id) or user.locale
        # Либо возвращаем значение языка из Базы Данных, либо если не было никакого ответа от user, то будет язык, который установлен в ТГ
        
        
        
def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)   #Теперь мы устонавливаем middleware на Dispatcher
    return i18n    #Возвращаемся i18n со всеми характиристиками, которые есть в ACLMiddleware
    