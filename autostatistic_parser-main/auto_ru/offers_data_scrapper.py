import sys
from pprint import pprint
from itertools import cycle
import re
import json
import datetime
from multiprocessing import Pool

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

from database import db_connect
from logger import get_logger
from selenium_driver import SeleniumDriver
from remove_emoji import remove_emoji
from sleep import scrapping_sleep
from duplicates import find_duplicates, add_duplicates_to_base
from transliterate import transliterate_title
from string_to_number import string_to_number
from lists_methods import slice_list

from common_config import LOGFILE_PATH, SELENIUM_WIRE_OPTIONS, LEXICON, OFFER_INFO_ROW_CLASSES, SCRAPE_DATA_PROCESSES_COUNT
from proxies import AUTO_RU_OFFER_SCRAPE_DATA_PROXIES
from platform_config import PLATFORM

logger = get_logger(__name__, LOGFILE_PATH)
processes_count = SCRAPE_DATA_PROCESSES_COUNT


def scrape_data(region='Санкт-Петербург'):
    """Scrapping data for offers that has been added recently.

    Args:
        region (string, optional): The region to check data. Defaults to "Санкт-Петербург"
    """

    logger.warning('Получаем добавленные предложения для сбора данных...')
    offers_to_scrape = get_offers_to_scrape(region)
    logger.warning(
        f'Количество предложений для сбора данных: {len(offers_to_scrape)}')

    if len(offers_to_scrape) == 0:
        return

    options = prepare_parsing_options(offers_to_scrape)

    if PLATFORM == 'linux64':
        display = Display()
        display.start()

    with Pool(processes=processes_count) as pool:
        pool.map(scrape_offer_data, options)

    if 'display' in locals():
        display.stop()


def scrape_offer_data(options):
    """Scrapping the offer data.

    Args:
        options (dict): The dictionary including scraping options and offers' data.
    """

    wire_options = options['wire_options']
    offers_data = options['offers_data']

    selenium_driver = SeleniumDriver()
    selenium_driver.init_driver(wire_options)

    connection = db_connect()
    cursor = connection.cursor()

    for offer_data in offers_data:
        offer_id = offer_data[0]
        offer_url = offer_data[1]
        offer_title = offer_data[2]

        try:
            logger.warning(
                f'Получаем исходный код для предложения c url {offer_url}...')
            page_source_code = selenium_driver.get_page_source(offer_url)
        except Exception as e:
            logger.warning(
                f'Ошибка во время парсинга предложения с id {offer_id}. Код ошибки: {e}. Прокси: {wire_options["proxy"]}')
            return

        offer_params = get_offer_params(page_source_code, offer_id)

        add_offer_data_to_base(connection, cursor, offer_params)
        duplicates = find_duplicates(cursor, offer_id)
        duplicated_ids = duplicates['ids']

        if len(duplicated_ids) > 0:
            add_duplicates_to_base(connection, cursor, duplicated_ids)

        transliterate_title(connection, cursor, offer_title)
        scrapping_sleep()

    selenium_driver.quit()
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
    data_attributes = soup.find(id='sale-data-attributes')
    offer_params = {}

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
    dealer_type = soup.find(
        class_='CardSellerNamePlace__owner-info_dealer')

    if dealer_type is not None:
        offer_params['seller_type'] = LEXICON['seller_type']['dealer']
    else:
        offer_params['seller_type'] = LEXICON['seller_type']['private_person']

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


def add_offer_data_to_base(connection, cursor, params):
    """Adding the offer's data to the base.

    Args:
        connection (mariadb.connection): The instance of 'mariadb.connection' class.
        cursor (mariadb.connection.cursor): The instance of 'mariadb.connection.cursor' class.
        params (dict): The offer' data to add.
    """

    offer_id = params['id']
    update_data = []

    for key, value in params.items():
        if key == 'id':
            continue

        if value is None:
            continue

        if isinstance(value, (int, float)):
            update_data.append(f'`{key}` = {value}')
        else:
            update_data.append(f'`{key}` = "{value}"')

    update_data.append(f'`checkedon` = "{datetime.datetime.now()}"')

    sql = '''
        UPDATE
            `offers_list`
        SET
            ''' + (',\n').join(update_data) + '''
        WHERE
            `id` = ''' + str(offer_id) + ''';
    '''

    try:
        cursor.execute(sql)
        connection.commit()
        logger.warning(f'Добавили данные для предложения с id {offer_id}.')
    except Exception as e:
        connection.rollback()
        logger.warning(
            f'Не удалось добавить данные для предложения с id {offer_id}. Ошибка: {e}')


def prepare_parsing_options(offers):
    """Preparing parsing options.

    Args:
        (list): The offers to scrape data.

    Returns:
        list: The list of options including `wire_options` and `offers_data`.
    """

    proxy_cycle = cycle(AUTO_RU_OFFER_SCRAPE_DATA_PROXIES)
    proxy = next(proxy_cycle)
    options = []

    sliced_offers = slice_list(offers, processes_count)
    options_count = min(len(sliced_offers), processes_count)

    for i in range(options_count):
        wire_options = SELENIUM_WIRE_OPTIONS.copy()
        wire_options['proxy'] = {
            'https': f'https://{proxy}'
        }
        options.append({
            'wire_options': wire_options,
            'offers_data': sliced_offers[i]
        })
        proxy = next(proxy_cycle)

    return options


def get_offers_to_scrape(region='Санкт-Петербург'):
    """Getting the offers to scrape data.

    Args:
        region (string): The region to filter offers.

    Returns:
        list: The list of offers data.
    """
    sql = '''
        SELECT
            id, url, title
        FROM
            offers_list
        WHERE
            url IS NOT NULL AND
            checkedon IS NULL AND
            region = "''' + region + '''"
        ORDER BY id ASC
    '''

    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    offers = cursor.fetchall()
    cursor.close()
    connection.close()

    return offers


if __name__ == '__main__':
    scrape_data()
