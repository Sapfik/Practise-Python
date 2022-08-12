from os import curdir
import sqlite3 as sql
from create_bot import  bot

def sql_start():
    global base, cur
    base = sql.connect('pizza.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
        base.execute ('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
        #CREATE TABLE IF NOT EXISTS - создать таблицу, если такой не существует
        base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?,?,?,?)', tuple(data.values()))
        # INSERT INTO menu VALUES(?,?,?,?) - ДЛЯ ТОГО, ЧТОБЫ ДАННЫЕ ЗАНОСИЛИСЬ В БД И БЫЛИ ЗАШИФРОВАННЫ ДЛЯ ДРУГИХ
        # tuple(data.values() - для удобства разработчика (данные заносятся в кортеж)
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():    #fetchall() - выгружает все данные из таблицы в список, который указан ниже
        await bot.send_photo (message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')


async def sql_read2 ():
    return cur.execute('SELECT * FROM menu').fetchall()

#sql_read2() - просто читает выборку(все позиции) из таблицы sqlite

async def sql_delete(data):    #data - название пиццы
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()

#sql_delete(data) - удаляет по названию конкретную пиццу 
