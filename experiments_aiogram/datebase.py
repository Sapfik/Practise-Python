from aiogram import types, Bot
from gino import Gino
# gino - более быстрая библиотека для создания таблицы в БД
from sqlalchemy import (Column, Integer, Boolean, JSON, TIMESTAMP, Sequence, String , BigInteger)
from sqlalchemy import sql
from gino.schema import GinoSchemaVisitor
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.operators import json_getitem_op

from config import db_pass, db_user, host

db = Gino()

class User (db.Model):   #Класс для юзера
    __tablename__ = 'users'
    id = Column(Integer, Sequence("user_id_seq"), primary_key = True)
    user_id  = Column(BigInteger)
    language = Column(String(2))     # цифра в скобках - это максимальное количество элементов
    fullname = Column(String(100))
    username = Column(String(100))
    referral = Column(Integer)
    query: sql.Select    #sql.Select - нужно для того, чтобы было легче писать код и для выборки элементов в таблицу и занесения их туда


class Item (db.Model):    # Класс для предмета
    __tablename__ = 'items'
    query : sql.Select
    id = Column(Integer, Sequence("user_id_seq"), primary_key = True)
    name = Column(String(50))
    photo = Column(String(100))
    price = Column(Integer)


class Purchase (db.Model):    # Класс для покупки
    __tablename__ = 'purchases'
    query : sql.Select
    
    id = Column(Integer, Sequence("user_id_seq"), primary_key = True)
    buyer = Column(BigInteger)
    item_id = Column(Integer)
    amount = Column(Integer)
    quanity = Column (Integer)
    purchase_time = Column(TIMESTAMP)
    shopping_adress = Column(JSON)    #Заносим в JSON так как адрес может быть любой
    phone_number = Column(String(50))
    email = Column(String(200))
    receiver = Column(String(100))
    successful = Column(Boolean, default=False)
    
    
    
class DBCommands:
    async def get_user (self, user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        # Если наш user_id, который в телеграм совпадает User.user_id, который так же является нашим айди в тг, то мы через gino заносим в колонку айди
        return user
    
    
    async def add_new_user(self, referral = None) -> User:
        user = types.User.get_current()    # Получаем данные от юзера
        old_user = await self.get_user(user.id)    # get_user - это функция, которую мы создали выше
        if old_user:    # Если такой юзер уже есть, то мы просто возвращаем значение функции
            return old_user
        
        new_user = User()    #Вызываем класс User для занесения данных о юзере в него
        
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.fullname = user.full_name
        
        if referral:      # Делаем проверку на то, есть ли реферал у нашего юзера
            new_user.referral = int(referral)  
        await new_user.create()
        return new_user
           
    
    async def set_language(self, language):
        user_id = types.User.get_current().id    #Получаем текущий айди пользователя
        user = await self.get_user(user_id)   #Делаем проверку на то, есть ли он уже в таблице
        await user.update(language=language).apply()   # Изменяем язык
        
    
    async def count_scalar (self):
        total = await db.func.count(User.id).gino.scalar()  # Подсичтываем сколько у нас всего айдишников в БД и переводим все в gino(конечное значение)
        return total
    
    
    async def check_referrals(self):
        bot = Bot.get_current()
        user_id = types.User.get_current().id  #Получаем текущий айди пользователя
        user = await self.get_user(user_id)    #Делаем проверку на то, есть ли он уже в таблице
        referrals = await User.query.where(User.referral == user.id).gino.all()  # Если у юзера есть реферрал, то мы показываем его(gino.all() - показывает всех реферралов, так как их может быть много)
        return ", ".join([
            f"{num+1}. " + (await bot.get_chat(referral.user_id)).get_mention(as_html=True) # Пишем номер реферрала, а затем и его имя
            for num, referral in enumerate(referrals)   #Нумеруем каждого реферрала
        ])
        
    async def show_items(self):
        items = await Item.query.gino.all()   #Делаем запросы к БД, которая будет отдавать все наши товары
        return items
    

async def create_db():  #Эту функцию мы будем использывать при зацпуске бота
    await db.set_bind(f"postgresql://{db_user}:{db_pass}@{host}/gino")    #Получаем доступ к БД
    await db.gino.create_all()   #Для просмотра БД
    await db.gino.drop_all()   #Для перезаписи БД
    await db.gino.create_all()    #Создается все по-новой
     