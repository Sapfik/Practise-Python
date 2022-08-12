import sys
import datetime
from pprint import pprint
import re

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

from selenium_driver import SeleniumDriver
from logger import get_logger
from database import db_connect
from sleep import scrapping_sleep

from common_config import LOGFILE_PATH, SELENIUM_WIRE_OPTIONS
from platform_config import PLATFORM

logger = get_logger(__name__, LOGFILE_PATH)

IDS_TO_REMOVE_FILE_PATH = 'docs/ids.txt'


def clean_regions():
    """Cleaning the regions
    """

    search_interval = datetime.datetime.now(
    ) - datetime.timedelta(days=20)

    sql = '''
        SELECT
            `id`,
            `url`
        FROM
            `offers_list`
        WHERE
            `checkedon` > "''' + str(search_interval) + '''"
    ;'''

    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()

    remaining_records = len(records) + 1

    logger.info(
        f'Предложений для проверки правильности регионов: {remaining_records}')

    if PLATFORM == 'linux64':
        display = Display()
        display.start()

    selenium_driver = SeleniumDriver()
    selenium_driver.init_driver(SELENIUM_WIRE_OPTIONS)

    with open('docs/cities.txt', 'r+', encoding='utf-8') as file:

        for record in records:
            remaining_records -= 1
            logger.info(f'Осталось предложений {remaining_records}')
            record = list(record)
            offer_id = record[0]
            url = record[1]

            logger.info(
                f'Проверяем регион для предложения с id {offer_id} и url {url}...')

            try:
                page_source_code = selenium_driver.get_page_source(url)
            except:
                logger.info(f'Не удалось получить данные для предложения.')
                continue

            soup = BeautifulSoup(page_source_code, 'html.parser')
            crumbs_texts = soup.find_all(class_='CardBreadcrumbs__itemText')

            if len(crumbs_texts) == 0:
                continue

            last_crumb_text = crumbs_texts[-1]

            city_r = re.sub(r'\s', ' ', last_crumb_text.get_text())
            city_r = re.sub(r'^\s', '', city_r)

            file.seek(0, 2)
            file.write(f'{city_r}\n')

            scrapping_sleep()

    cursor.close()
    connection.close()
    selenium_driver.quit()

    if 'display' in locals():
        display.stop()


def get_cities_from_file(cities_file_path):
    """Getting the list of cities to remain.

    Args:
        cities_file_path (str): The relative file path.

    Returns:
        list: The list of cities to remain.
    """

    cities = []

    with open(cities_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            city = re.sub(r'\n', '', line)
            cities.append(city)

    return cities


def find_ids_to_clean():
    """Finding the offers ids to clean. Writing them to file.
    """

    cities = get_cities_from_file('docs/cities.txt')
    search_interval = datetime.datetime.now(
    ) - datetime.timedelta(days=35)

    sql = '''
        SELECT
            `id`,
            `url`
        FROM
            `offers_list`
        WHERE
            `createdon` > "''' + str(search_interval) + '''"
    ;'''

    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()

    remaining_records = len(records) + 1

    logger.info(
        f'Предложений для проверки правильности регионов: {remaining_records}')

    if PLATFORM == 'linux64':
        display = Display()
        display.start()

    selenium_driver = SeleniumDriver()
    selenium_driver.init_driver(SELENIUM_WIRE_OPTIONS)

    with open(IDS_TO_REMOVE_FILE_PATH, 'r+', encoding='utf-8') as file:
        for record in records:
            remaining_records -= 1
            logger.info(f'Осталось предложений {remaining_records}')
            record = list(record)
            offer_id = record[0]
            url = record[1]

            logger.info(
                f'Проверяем регион для предложения с id {offer_id} и url {url}...')

            try:
                page_source_code = selenium_driver.get_page_source(url)
            except:
                logger.info(f'Не удалось получить данные для предложения.')
                continue

            soup = BeautifulSoup(page_source_code, 'html.parser')
            crumbs_texts = soup.find_all(class_='CardBreadcrumbs__itemText')

            if len(crumbs_texts) == 0:
                continue

            last_crumb_text = crumbs_texts[-1]

            city_r = re.sub(r'\s', ' ', last_crumb_text.get_text())
            city_r = re.sub(r'^\s', '', city_r)

            if city_r not in cities:
                file.seek(0, 2)
                file.write(f'{offer_id}\n')
                logger.info(
                    f'Добавил id предложения {offer_id}. Город в объявлении: {city_r}')

            scrapping_sleep()

    cursor.close()
    connection.close()
    selenium_driver.quit()

    if 'display' in locals():
        display.stop()


def write_in_file(city_r):
    """Writting the city to file

    Args:
        city_r (str): The city name.
    """

    with open('docs/cities.txt', 'r+', encoding='utf-8') as file:
        for line in file:
            if city_r in line:
                return

        file.seek(0, 2)
        file.write(f'{city_r}\n')


def remove_excessed_offers():
    """Removing offers from excessed regions.
    """

    excessed_ids = []

    with open(IDS_TO_REMOVE_FILE_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            excessed_ids.append(re.sub(r'\n', r'', line))

    connection = db_connect()
    cursor = connection.cursor()

    sql = '''
        DELETE
        FROM
            offers_list
        WHERE
            id IN (''' + ','.join(excessed_ids) + ''')
    ;'''

    try:
        logger.info('Удаляем предложения с «неправильными» регионами...')
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        logger.warning(f'Во время удаления предложений произошла ошибка: {e}')

    cursor.close()
    connection.close()


if __name__ == '__main__':
    remove_excessed_offers()
