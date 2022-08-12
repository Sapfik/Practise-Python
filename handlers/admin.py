from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state   
#FSMContext - позволяет менять машину состояний, чтобы программа подстраивалась в какой-то момент времени, под какое-то состояние
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from create_bot import dp, bot
from aiogram.dispatcher.dispatcher import  Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb


ID = None

class FSMAdmin (StatesGroup):    #class FSMAdmin - позволяет нам задать состояния для проги 
    photo = State()
    name = State()
    description = State()
    price = State()


#Получаем ID модератора 
@dp.message_handler(commands=['moderator'], is_chat_admin = True)
async def make_changes (message:types.Message):
    global ID

    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что вам нужно, хозяин???', reply_markup=admin_kb.button_case_admin)
    await message.delete()
    # else:
    #     await message.reply('Вы не являетесь администратором этой группы')

# Начало диалога, загрузки нового меню
@dp.message_handler(Text(equals='Заказать'))
async def cm_start (message:types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.answer('Загрузите фото')
        await message.delete()

# Команда для прерывания машины состояний
async def cancel_command(message:types.Message, state:FSMAdmin):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.delete()
        await message.answer('Ваш заказ был успешно отменен')


# Получаем первый ответ и пишем в словарь
async def load_photo (message:types.Message, state:FSMAdmin):  #state:FSMAdmin - указываем какую именно мы использываем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:     #state.proxy() - записывает фотографии в список в состояния(на данный момент это photo)
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введите пожалуйста название пиццы')

# Получаем второй ответ и пишем словарь
async def register_name(message:types.Message, state:FSMAdmin):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите пожалуйста описание для пиццы')

# Получаем третий ответ и пишем словарь 
async def register_description (message:types.Message, state:FSMAdmin):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите цену, за которую вы можете её взять')


# Получаем последний ответ и заносим в словарь
async def register_price(message:types.Message, state:FSMAdmin):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            
            data['price'] = float(message.text)
                
            await message.answer('Вы удачно сделали заказ!')
                
        
        
        await sqlite_db.sql_add_command(state)
        await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def delete_position(callback:types.CallbackQuery):
    await sqlite_db.sql_delete(callback.data.replace('del ', ''))
    mark = callback.data.replace('del ', '')
    await callback.answer(text = f'{mark} удалена.', show_alert=True)


@dp.message_handler(commands=['Удалить'])
async def delte_pizza(message:types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
            await bot.send_message(message.from_user.id, text = '^^^', reply_markup = InlineKeyboardMarkup().\
                                add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}' )))


                                                                                

        

def register_handlers_admin(dp:Dispatcher):
    # dp.register_message_handler(make_changes, commands=['moderator'], is_chat_admin = True)
    dp.register_message_handler(cm_start, commands = 'Загрузить', state = None)
    dp.register_message_handler(cm_start, Text(equals='загрузить', ignore_case=True), state="*")
    dp.register_message_handler (cm_start, lambda message: 'заказать' in message.text)
    dp.register_message_handler (cm_start, lambda message: 'Заказать' in message.text)
    dp.register_message_handler (cm_start, Text(equals='Заказать', ignore_case=True))
    dp.register_message_handler(cancel_command, state = "*", commands='Отменить')
    dp.register_message_handler(cancel_command, Text(equals='отменить', ignore_case=True), state="*")
    dp.register_message_handler (cancel_command, lambda message: 'отменить' in message.text)
    dp.register_message_handler (cancel_command, lambda message: 'Отменить' in message.text)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(register_name, state = FSMAdmin.name)
    dp.register_message_handler(register_description, state=FSMAdmin.description)
    dp.register_message_handler(register_price, state= FSMAdmin.price)
    