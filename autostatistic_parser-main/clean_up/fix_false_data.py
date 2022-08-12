import sys
import datetime
from pprint import pprint
import json
import re

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

from selenium_driver import SeleniumDriver
from logger import get_logger
from database import db_connect
from sleep import scrapping_sleep
from offers_data_scrapper import add_offer_data_to_base
from remove_emoji import remove_emoji
from string_to_number import string_to_number

from common_config import LOGFILE_PATH, SELENIUM_WIRE_OPTIONS, LEXICON
from platform_config import PLATFORM

logger = get_logger(__name__, LOGFILE_PATH)

OFFER_INFO_ROW_CLASSES = {
    'body': 'CardInfoRow_bodytype',
    'color': 'CardInfoRow_color',
    'engine': 'CardInfoRow_engine',
    'tax': 'CardInfoRow_transportTax',
    'transmission': 'CardInfoRow_transmission',
    'drive': 'CardInfoRow_drive',
    'hand_drive': 'CardInfoRow_wheel',
    'condition': 'CardInfoRow_state',
    'owners': 'CardInfoRow_ownersCount',
    'pts': 'CardInfoRow_pts',
    'possession_time': 'CardInfoRow_owningTime',
    'customs': 'CardInfoRow_customs',
    'guarantee': 'CardInfoRow_warranty',
    'release_year': 'CardInfoRow_year'
}

BLOCKED_IDS_FILE_PATH = 'docs/blocked_ids.txt'
FIXED_IDS_FILE_PATH = 'docs/fixed_ids.txt'
CREATEDON_FROM = '2021-08-19 16:39:00'
CREATEDON_TO = '2021-09-03 20:41:00'


def fix_false_data():
    """Fixing the false data that has been added due to auto.ru protection.
    """

    connection = db_connect()
    offers_to_check = get_offers_to_check(connection)

    logger.info(
        f'Предложений для проверки корректных данных: {len(offers_to_check)}')
    remaining_offers = len(offers_to_check) + 1

    if PLATFORM == 'linux64':
        display = Display()
        display.start()

    selenium_driver = SeleniumDriver()
    selenium_driver.init_driver(SELENIUM_WIRE_OPTIONS)

    cursor = connection.cursor()

    for offer in offers_to_check:
        remaining_offers -= 1
        logger.info(
            f'Oсталось предложений для проверки {remaining_offers}')

        url = offer['url']
        offer_id = offer['offer_id']

        old_engine_type = offer['engine_type']
        old_release_year = offer['release_year']
        old_transmission = offer['transmission']
        old_run = offer['run']

        try:
            logger.warning(
                f'Получаем исходный код для предложения с url {url}...')
            page_source_code = selenium_driver.get_page_source(url)
            scrapping_sleep()
        except Exception as e:
            logger.warning(
                f'Ошибка во время парсинга предложения с id {offer_id}. Код ошибки: {e}.')
            continue

        logger.info(
            f'Проверяем предложение с id {offer_id} и url {url}...')

        offer_params = get_offer_params(page_source_code, offer_id)

        if 'status' in offer_params and offer_params['status'] == 'Blocked':
            with open(BLOCKED_IDS_FILE_PATH, 'r+', encoding='utf-8') as file:
                file.seek(0, 2)
                file.write(f'{offer_id}\n')

            continue

        if offer_params['run'] != old_run or \
                offer_params['engine_type'] != old_engine_type or \
                int(offer_params['release_year']) != old_release_year or \
                offer_params['transmission'] != old_transmission:

            logger.info(
                f'У предложения с id {offer_id} и url {url} неверные данные, нужно обновить.')

            with open(FIXED_IDS_FILE_PATH, 'r+', encoding='utf-8') as file:
                file.seek(0, 2)
                file.write(f'{offer_id}\n')

            add_offer_data_to_base(connection, cursor, offer_params)

    selenium_driver.quit()

    if 'display' in locals():
        display.stop()

    cursor.close()
    connection.close()


def get_offer_params(page_source_code, offer_id):
    """Getting offer's params from its source code.

    Args:
        page_source_code (str): The offer' page source code.
        offer_id (int): The offer's id.

    Returns:
        dict: The dictionary with offers' data.
    """

    soup = BeautifulSoup(page_source_code, 'html.parser')

    listing_container_element = soup.find(class_='PageListing')

    offer_params = {}

    if listing_container_element is not None:
        offer_params['status'] = 'Blocked'
        logger.info(f'Предложение с id {offer_id} заблокировано.')
        return offer_params

    data_attributes = soup.find(id='sale-data-attributes')

    if data_attributes is not None:
        data_attributes = data_attributes.get('data-bem')
        data_attributes = json.loads(data_attributes)
        offer_params['id'] = offer_id

        if 'markName' in data_attributes['sale-data-attributes']:
            offer_params['brand'] = data_attributes['sale-data-attributes']['markName']
        else:
            offer_params['brand'] = None

        if 'modelName' in data_attributes['sale-data-attributes']:
            offer_params['model'] = data_attributes['sale-data-attributes']['modelName']
        else:
            offer_params['model'] = None

        if 'km-age' in data_attributes['sale-data-attributes']:
            offer_params['run'] = int(
                data_attributes['sale-data-attributes']['km-age'])
        else:
            offer_params['run'] = None

        if 'power' in data_attributes['sale-data-attributes']:
            offer_params['power'] = int(
                data_attributes['sale-data-attributes']['power'])
        else:
            offer_params['power'] = None

        if 'price' in data_attributes['sale-data-attributes']:
            offer_params['price'] = int(
                data_attributes['sale-data-attributes']['price'])
        else:
            offer_params['price'] = None

    description = soup.find(class_='CardDescription__textInner')

    if description is not None:
        description = remove_emoji(
            description.get_text()).replace('"', '\\"')
        offer_params['description'] = description
    else:
        offer_params['description'] = None

    info_rows = soup.find_all(class_='CardInfoRow')
    configuration_title = soup.find(class_='CardComplectation__title')

    if configuration_title is not None:
        configuration_text = configuration_title.get_text().replace(
            LEXICON['configuration']['label'], '').strip()
        if configuration_text == '':
            offer_params['configuration'] = LEXICON['configuration']['values']['undefined']
        else:
            offer_params['configuration'] = configuration_text.replace(
                '"', '\\"')

    if len(info_rows) > 0:
        for info_row in info_rows:
            if info_row['class']:
                for option in OFFER_INFO_ROW_CLASSES:
                    if OFFER_INFO_ROW_CLASSES[option] in info_row['class']:

                        if option == 'engine':
                            engine_params = info_row.contents[1].get_text().split(
                                ' / ')
                            if len(engine_params) > 0:
                                if engine_params[0] is not None:
                                    engine_volume = re.sub(
                                        r'[^0-9.]+', r'', engine_params[0])
                                    engine_volume = re.sub(
                                        r'\.+$', r'', engine_volume)
                                    offer_params['engine_volume'] = float(
                                        engine_volume)
                                else:
                                    offer_params['engine_volume'] = None

                                if engine_params[2] is not None:
                                    offer_params['engine_type'] = engine_params[2]
                                else:
                                    offer_params['engine_type'] = None

                        else:
                            option_value = info_row.contents[1].get_text()

                            if option in ['tax']:
                                option_value = string_to_number(
                                    option_value)
                            offer_params[option] = option_value
    return offer_params


def get_offers_to_check(connection):
    """Getting the list of offers to check corrupted data.

    Args:
        connection (mariadb.connection): The instance of 'mariadb.connection' class.

    Returns:
        list: The list of offers to check.
    """

    sql = '''
        SELECT
            `id`,
            `title`,
            `engine_type`,
            `release_year`,
            `transmission`,
            `run`,
            `url`
        FROM
            `offers_list`
        WHERE
            `createdon` BETWEEN "''' + CREATEDON_FROM + '''" AND "''' + CREATEDON_TO + '''"
        ORDER BY
            `id` ASC
        LIMIT 1000
        OFFSET 140
    ;'''

    cursor = connection.cursor()
    cursor.execute(sql)
    offers = cursor.fetchall()
    cursor.close()

    offers = list(map(lambda x: {
        'offer_id': x[0],
        'title': x[1],
        'engine_type': x[2],
        'release_year': x[3],
        'transmission': x[4],
        'run': x[5],
        'url': x[6]
    }, offers))

    return offers


def fix_fixed_offers_price():
    """Fixing the fixed offers price.
    """

    fixed_ids = []

    with open(FIXED_IDS_FILE_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            fixed_ids.append(int(re.sub(r'\n', r'', line)))

    connection = db_connect()
    cursor = connection.cursor()

    for fixed_id in fixed_ids:
        logger.info(f'Сбрасываем цену для предложения с id {fixed_id}...')
        sql = '''
            UPDATE
                offers_list
            SET
                price = NULL
            WHERE
                id = ''' + str(fixed_id) + '''

        ;'''

        try:
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            logger.warning(
                f'Что-то пошло не так при обновлении предложения с id {fixed_id}. Текст ошибки {e}')

    cursor.close()
    connection.close()


def remove_blocked_offers():
    """Removing blocked offers.
    """

    blocked_ids = []

    with open(BLOCKED_IDS_FILE_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            blocked_ids.append(re.sub(r'\n', r'', line))

    connection = db_connect()
    cursor = connection.cursor()
    blocked_ids = ','.join(blocked_ids)

    sql = '''
        DELETE
        FROM
            offers_list
        WHERE
            id IN (''' + blocked_ids + ''')
    ;'''

    try:
        logger.info('Удаляю заблокированные предложения...')
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        logger.warning(f'Во время удаления возникла ошибка: {e}')

    cursor.close()
    connection.close()


def remove_tracking_entries():
    """Removing the currupted offers' tracking entries.
    """

    connection = db_connect()
    cursor = connection.cursor()

    sql = '''
        DELETE
        FROM
            offers_tracking
        WHERE
            checkedon BETWEEN "''' + CREATEDON_FROM + '''" AND "''' + CREATEDON_TO + '''" AND
            status IS NULL
    ;'''

    try:
        logger.info('Удаляю информацию об изменении цены...')
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        logger.warning(
            f'Во время удаления информации об изменении цены возникла ошибка: {e}')

    cursor.close()
    connection.close()


if __name__ == '__main__':
    fix_false_data()
