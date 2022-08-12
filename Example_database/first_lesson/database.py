import sqlite3
from random import randint
from sqlite3.dbapi2 import PARSE_DECLTYPES

global db
global sql
db = sqlite3.connect('server.db')   #Создаем базу данных и подключаемся к ней
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (     
    login TEXT,
    password TEXT,
    cash BIGINT
    )""")    #Создаем таблицу в базе данных

db.commit()    #Подвтверждаем создание таблицы

def reg():
    user_login = input('Login: ')
    user_password = input('Password: ')

    sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")    #Выбираем столбец login в таблице users

    if sql.fetchone() is None:   #Если такого логина еще нету, то мы создаем ему логин пароль и кэш
        sql.execute("INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, 0))   
        db.commit()   #Подтверждаю данные
        
        print('Зарегистрирован!') 
    else:
        print('Такая запись уже имеется!')
        
        for value in sql.execute("SELECT * FROM users"):
            print(value)
            
def delete_db():
    sql.execute(f"DELETE FROM users WHERE login = '{user_login}'")    #Удаляем логин человека из таблицы users, если он проиграл в казино
    db.commit()
    
    print('Запись была удалена!')
            
def casino():
    global user_login
    user_login = input('Log in: ')
    number = randint(1, 2)
    
    # for i in sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'"):
    #     balance = i[0]    #для прибовления баланса выбираем строку cash в таблице и присваиваем к переменно balance значение это строки 
    try:
        sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
        balance = sql.fetchone()[0]
    except:
        pass
    
    sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
    if sql.fetchone() is None:      #Проверяем нету ли такого пользователя, если нет, то перекидываем его в функцию reg()
        print('Зарегистрируйтесь')
        reg()
        
    else:
        if number == 1:
            sql.execute(f"UPDATE users SET cash = {1000 + balance} WHERE login = '{user_login}'")     #Добавляем к балансу 1000 юзеру под таким то логином
            db.commit()
            print(f'{user_login} выйграл в этом смертельном казино')
        else:
            print('Вы проиграли')
            delete_db()
            
def enter():
    # for i in sql.execute("SELECT login, cash FROM users"):     #Выбираем login и cash из таблицы users
    #     print(i)
    
    sql.execute("SELECT login, cash FROM users")
    row = sql.fetchall()
    print(row)
        
def main():
    casino()
    enter()
    
main()    
