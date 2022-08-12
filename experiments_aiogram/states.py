from aiogram.dispatcher.filters.state import StatesGroup, State

class Purchase(StatesGroup):    #Класс-состояние для покупки товаров
    EnterQuanity  = State()   # Вводим количество
    Approval = State()    #Подтверждение того, что мы все правильно ввели
    Payment = State()   # Состояние оплаты
    

class NewItem(StatesGroup):    #Класс-состояние для создания товара
    Name  = State()
    Photo = State()
    Price = State()
    Confirm = State()   #Состояние подтверждения изменений
    
    
class Mailing (StatesGroup):   #Класс-состояние - для рассылки
    Text = State()   
    Language = State()
    
    
    