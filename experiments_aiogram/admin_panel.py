from asyncio import sleep
from typing import Text

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import inline_keyboard, user

from load_all import bot, dp, _
from config import admin_id
from states import NewItem, Mailing

from datebase import Item, User


@dp.message_handler(user_id = admin_id, commands='cancel')
async def cancel(message:types.Message, state:FSMContext):
    await message.answer(_("Вы отменили создание товара"))
    await state.reset_state()    #reset_state() - отменяет состояние преждевременно
    

@dp.message_handler(user_id = admin_id,commands='add_item')   #К этому handlery имеет доступ только админ
async def add_item(message:types.Message):
    await message.answer(_("Введите название или нажмите на /cancel"))   # _  - для перевода текста на другие языки
    await NewItem.Name.set()
    
    
@dp.message_handler(user_id = admin_id, state=NewItem.Name)
async def enter_name(message:types.Message, state:FSMContext):
    name = message.text
    item = Item()
    item.name = name
    await message.answer(_("Название: {name}"
                           "\nПришлите мне фотографию товара, а не документ или нажмите /cancel").format(
                            name = name
                        ))
    
    await NewItem.Photo.set()    #Устанавливаем новые state
    await state.update_data(item=item)   #Передаем сохраненную информацию о нашем товаре в нашу Машину Состояний
    

@dp.message_handler(user_id = admin_id, state = NewItem.Photo, content_types=types.ContentType.PHOTO)  #Задает изначально тип функции
async def add_photo(message:types.Message, state : FSMContext):
    photo = message.photo[-1].file_id   #Получаем айди фото
    data = await state.get_data()    #Получаем данные состояния
    item: Item = data.get('item')
    # item: Item тоже самое, что и item = Item()
    
    item.photo = photo     #Заносим в БД фото
    
    await message.answer_photo(
        photo = photo,
        caption = _("Название {name}"
                    "\nПришлите мне цену в копейках или нажмите на команду /cancel").format(
                        name = item.name
                    )
                )
    
    await NewItem.Price.set()     #Переходим к состоянию о цене
    await state.update_data(item = item)    #Обновляем БД
    

@dp.message_handler(user_id = admin_id, state = NewItem.Price)   
async def enter_price(message:types.Message, state: FSMContext):
    data = await state.get_data()    #Получаем данные состояния
    item: Item = data.get('item')
    
    try:
        price = int(message.text)
    except ValueError:
        await message.answer(_("Неверное значение, введите число!"))
        return
    
    item.price = price
    
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text = _('Да'),
                callback_data = 'confirm')],  
            
            [types.InlineKeyboardButton(
                text = _('Ввести заново'),
                callback_data='change'
            )]
        ]
    )
    
    await message.answer(
        _("Цена: {price:,}\n"
          "Подтверждаете?Нажмите на /cancel, чтобы отменить").format(price=price),
        reply_markup=markup
    )
    
    await state.update_data(item = item)
    await NewItem.Confirm.set()
    

@dp.callback_query_handler(user_id = admin_id, text_contains = "change", state = NewItem.Confirm)
async def change_price(call:types.CallbackQuery):   
    await call.message.edit_reply_markup()   #Для того, чтобы убрать клавиатуру (это делает edit_reply_markup)
    await call.message.answer(_("Введите заново цену товара в копейках"))
    await NewItem.Price.set()
    
    
@dp.callback_query_handler(user_id = admin_id, text_contains = "confirm", state = NewItem.Confirm)
async def confirm(call:types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()    #Убираем клавиатуру
    data = await state.get_data()
    item: Item = data.get('item')
    await item.create()    #Заносим все состояния(имя, фото, цену) в БД
    
    await call.message.answer(_("Товар удачно создан!"))
    await state.reset_state()   #Заканчиваем состояние
    

@dp.message_handler(user_id = admin_id, commands='tell_everyone')
async def mailing(message:types.Message):
    await message.answer(_("Пришлите текст для рассылки"))
    await Mailing.Text.set()
    
@dp.message_handler(user_id = admin_id, state = Mailing.Text)
async def enter_text(message:types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text = text)
    
    markup = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(
            text = 'Русский',
            callback_data = 'ru')],  
        
        [types.InlineKeyboardButton(
            text ='English',
            callback_data='en'
        )],
        
        [types.InlineKeyboardButton(
           text = 'Українська',
           callback_data='uk'
        )]
    ]
)
        
    await message.answer(_("На каком языке разослать это сообщение?\n\n"
                           "Текст:\n"
                           "{text}").format(text=text),
                         reply_markup=markup)
    
    await Mailing.Language.set()
    
    
@dp.callback_query_handler(user_id = admin_id, state = Mailing.Language)
async def enter_language(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    await state.reset_state()
    await call.message.edit_reply_markup()   #Удаляем клавиатуру
    users = await User.query.where(User.language == call.data).gino.all()   #Собираем всех юзеров у которых установлен язык какой-либо
    
    for user in users:
        try:
            await bot.send_message(chat_id=user.user_id,
                                   text = text)
            
            await sleep(0.3)
            
        except Exception:
            pass
        
        await call.message.answer(_("Рассылка успешно выполнена"))


    
