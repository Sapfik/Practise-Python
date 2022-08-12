from asyncio import sleep
import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, state
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery,LabeledPrice,PreCheckoutQuery, order_info, reply_keyboard, shipping_address

from aiogram.utils.callback_data import CallbackData

import datebase
import states
from config import admin_id, lp_token
from load_all import dp, bot, _

db = datebase.DBCommands()    #Включаем все данные из БД  и читаем их
 
buy_item = CallbackData("buy", "item_id")    # Первое это то, что мы хотим купить, а второй пункт это под каким личным id этот предмет будет

@dp.message_handler(CommandStart())    #CommandStart - тоже самое, что и commands = 'start'
async def register_user(message:Message):
    chat_id = message.from_user.id
    referral = message.get_args()    #Получаем реферрала
    user = await db.add_new_user(referral=referral)   #Создаем нового юзера, если его еще нету
    id = user.id  #Получаем внутрений айди телеграма
    
    ############   Для создания реферальной ссылки  ############ 
    bot_username = (await bot.me).username   #Получаем username бота
    bot_link = f"https://t.me/{bot_username}?start={id}"   #Реферальная ссылка
    
    languages_markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text = 'Русский',
                callback_data = 'lang_ru')],  
            
            [types.InlineKeyboardButton(
                text ='English',
                callback_data='lang_en'
            )],
            
            [types.InlineKeyboardButton(
            text = 'Українська',
            callback_data='lang_uk'
            )]
        ]
    )
    count_users = await db.count_scalar()
    
    text = _("Приветствую вас!!!\n"
             "Сейчас в базе {count_users} человека!\n"
             "\n"
             "Ваша реферальная ссылка {bot_link}\n"
             "Проверить рефералов можно по команде /referrals\n"
             "Просмотреть товары по команде /items").format(
                 count_users = count_users,
                 bot_link = bot_link
                 
             )
             
    if message.from_user.id == admin_id:    #Если сообщение отослал админ, то мы добавляем к тексту еще одну строку
        text += _("\n"
                 "Добавить новый товар можно по команде /add_item")
        
    await message.answer(text,reply_markup=languages_markup)
    ############   Для создания реферальной ссылки  ############ 
    
 
@dp.callback_query_handler(text_contains = "lang")  #Если человек нажал на клавиатуру  
async def change_language(call: CallbackQuery):
    await call.message.edit_reply_markup()    #Убираем клавиатуру
    lang = call.data[-2:]   #Забираем 2 последних элемента (en, uk, ru)
    await db.set_language(language=lang)   #Нажми и посмотри на эту функцию 
    await call.message.answer(_("Ваш язык был изменен", locale=lang))   #locale = lang - Задаем новый язык или это можно назвать локаль
    
@dp.message_handler(commands = 'referrals')    
async def check_referrals(message:Message):
    referrals = await db.check_referrals()    #Также нажми на check_referrals и посмотри что оно делает
    text = _("Ваши рефералы:\n{referrals}").format(referrals=referrals)
    
    await message.answer(text)
    
@dp.message_handler(commands='items')
async def show_items (message:Message):  
    all_items = await db.show_items()  #Достаем все товары из базы данных
    
    for item in all_items:
        text = _("<b>Товар</b> \t№{id}: <u>{name}</u>\n"
                 "<b>Цена</b> \t{price:,}\n")
    
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text = _("Купить"),
                    callback_data=buy_item.new(item_id = item.id)
                )]
            ]
        )
        
        await message.answer_photo(
            photo = item.photo,
            caption = text.format(id = item.id,
                                  name= item.name,
                                  price = item.price / 100),
            
            reply_markup=markup
        )
        
        await sleep(0.3)
        
@dp.callback_query_handler(buy_item.filter())   #Обработка ответа через .filter()        
async def buying_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = int(callback_data.get('item_id'))     #Передаем item_id, который указали в CallbackData (выше)   
    await call.message.edit_reply_markup()   #Убираем клавиатуру
    item = await datebase.Item.get(item_id)     #Получаем объект товара
    
    if not item:     #Если нету такого товара
        await call.message.answer(_("Такого товара не существует"))
        return
    
    text = _("Вы хотите купить товар \"<b>{name}</b>\" по цене <i>{price:,}/шт</i>\n"
             "Введите количество или нажмите отмена").format(name = item.name,
                                                             price = item.price / 100)
             
    await call.message.answer(text)
    await states.Purchase.EnterQuanity.set()     #Переходим в состояние для ввода количества
    
    await state.update_data(
        item = item,
        purchase = datebase.Purchase(
            item_id = item_id,
            purchase_time = datetime.datetime.now(),
            buyer = call.from_user.id
        )
    )
    
@dp.message_handler(regexp=r'^(\d+)$', state = states.Purchase.EnterQuanity)   #^ - начала строки, $ - окончание строки, /d+ - цифры, которые у нас указываются
async def enter_quantity(message:Message, state: FSMContext):
    quantity = int(message.text)
    async with state.proxy() as data:
        data['purchase'].quantity = quantity    # Сразу записываем количество в datebase.Purchase 
        item = data.get('item')
        amount = item.price * quantity
        data['purchase'].amount = amount     # Сразу записываем все в datebase.Purchase
        
    agree_button = InlineKeyboardButton(
        text = _("Согласен"),
        callback_data="agree"
    )
    
    change_button = InlineKeyboardButton(
        text = _("Ввести количество заново"),
        callback_data="change"
    )
    
    cancel_button = InlineKeyboardButton(
        text = _("Отменить покупку"),
        callback_data="cancel"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [agree_button],
            [change_button],
            [cancel_button]
        ]
    )
    
    await message.answer(
        _("Хорошо, вы хотите купить <i>{quantity}</i> {name} по цене <b>{price:,}/шт</b>\n\n"
          "Получится <b>{amount:,}</b>. Подтверждаете?").format(
              quantity = quantity,
              name = item.name,
              amount = amount / 100,
              price = item.price / 100
          ), reply_markup=markup
    )
    
    await states.Purchase.Approval.set()   
    
@dp.message_handler(state = states.Purchase.EnterQuanity)    #Все что не попало в предыдущий handler, попадает сюда
async def wrong_quantity(message:Message):
    await message.answer(_("Вы ввели неверное число!"))
    

@dp.callback_query_handler(text_contains = 'cancel', state = states.Purchase.Approval)
async def cancel_purchase(call:CallbackQuery, state : FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer(_("Вы отменили покупку!"))
    await state.reset_state()    #Выходим из состояния 
    
@dp.callback_query_handler(text_contains = 'change', state = states.Purchase.Approval)
async def change_purchase(call: CallbackQuery, state : FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer(_("Введите количество товара заново."))
    await states.Purchase.EnterQuanity.set()    #Если человек вводит change, то мы возвращаемся назад и отрабатываем EnterQuanity
    
@dp.callback_query_handler(text_contains = "agree", state=states.Purchase.Approval)
async def agree_purchase(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()    
    purchase = data.get('purchase')
    item = data.get('item')
    await purchase.create()   #Это создаст запись в БД
    await call.message.answer(
        _("Хорошо. Оплатите <b>{amount:,}</b> по методу указаному ниже и нажмите "
          "на кнопку ниже").format(amount = purchase.amount / 100)
    )
    
    ############   Делаем платежную систему  ############ 

    currency = "RUB"
    need_name = True
    need_phone_number = False
    need_email = False
    need_shopping_address = True
    
    await bot.send_invoice(       #Передаем счет
        chat_id = call.from_user.id,
        title = item.name,
        description=item.name,
        payload=str(purchase.id),
        start_parameter=str(purchase.id),
        currency = currency,
        prices=[
            LabeledPrice(label=item.name,
                         amount = purchase.amount)
        ],
        provider_token=lp_token,
        need_email=need_email,
        need_name=need_name,
        need_phone_number=need_phone_number,
        need_shipping_address=need_shopping_address
        )    
    
    await state.update_data(purchase = purchase)
    await states.Purchase.Payment.set() 
    
    ############   Делаем платежную систему  ############ 


@dp.pre_checkout_query_handler(state=states.Purchase.Payment)
async def checkout(query: PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(query.id, True)    #Списываем средства с человека, который оплатил
    data = await state.get_data()
    purchase: datebase.Purchase = data.get('purchase')
    succes = await check_payment(purchase)    #Проверяем статус оплаты
    
    if succes:
        await purchase.update(
            successful = True,
            shippings_adress = query.order_info.shipping_address.to_python()
            if query.order_info.shipping_address else None,
            phone_number = query.order_info.phone_number,     #order_info - сохраняет
            receiver = query.order_info.name,
            email = query.order_info.email
        ).apply()
        
        await state.reset_state()
        await bot.send_message(chat_id=query.from_user.id, text = _("Спасибо за покупку"))
        
    else:
        await bot.send_message(chat_id=query.from_user.id, text = _("Покупка не была подтверждена, попробуйте позже..."))

async def check_payment(purchase: datebase.Purchase):
    return True


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)
