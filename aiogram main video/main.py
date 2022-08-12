import asyncio
from asyncio import tasks 

async def count (counter):
    print (f'Количество элементов в counter = {len(counter)}')
    while True:
        await asyncio.sleep(1/1000)
        counter.append(1)

async def every_one_second (counter):
    while True:
        await asyncio.sleep(1)
        print (f'- 1 сек', f'Количество элементов в counter = {len(counter)}') 

async def every_five_seconds ():
    while True:
        await asyncio.sleep(5)
        print (f'---- 5 сек')

async def every_ten_seconds():
    while True:
        await asyncio.sleep(10)
        print (f'-------- 10 сек')


async def main ():
    counter  = list()
    tasks = [
    count(counter),
    every_one_second(counter),
    every_five_seconds(),
    every_ten_seconds()
    ]
    

    
    await asyncio.gather (*tasks)

    

asyncio.run(main())