import sys
import datetime
import json
from itertools import cycle
from pprint import pprint
from multiprocessing import Pool

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

from logger import get_logger
from selenium_driver import SeleniumDriver
from database import db_connect
from sleep import scrapping_sleep
from lists_methods import slice_list

from common_config import LOGFILE_PATH, CHECK_SOLD_PROCESSES_COUNT, SELENIUM_WIRE_OPTIONS, FOR_SALE_AGAIN_CHECK_DAYS
from proxies import AUTO_RU_CHECK_SOLD_PROXIES
from platform_config import PLATFORM

logger = get_logger(__name__, logfile=LOGFILE_PATH)
processes_count = CHECK_SOLD_PROCESSES_COUNT


def check_sold_offers(region='Санкт-Петербург'):
    """Checking the sold offers if their status has been changed.

    Args:
        region (str, optional): The check to check offers. Defaults to 'Санкт-Петербург'.
    """
    logger.warning('Начало проверки статуса «Продан».')

    date_to_compare = datetime.datetime.now(
    ) - datetime.timedelta(days=FOR_SALE_AGAIN_CHECK_DAYS)
    date_to_compare = '{:%Y-%m-%d %H:%M%:%S}'.format(date_to_compare)

    connection = db_connect()
    cursor = connection.cursor()
    sql = '''
        SELECT
            `id`, `url`, `price`
        FROM
            `offers_list`
        WHERE
            `status` IN("Sold", "Blocked")
        AND `checkedon` > "''' + str(date_to_compare) + '''"
        AND `region` = "''' + region + '''"
    '''
    cursor.execute(sql)
    records = cursor.fetchall()
    cursor.close()

    if len(records) == 0:
        logger.warning(
            'Нет предложений со статусом «Продан» или «Заблокировано».')
        return

    logger.warning(
        f'Найдено записей со статусом «Продан» или «Заблокировано»: {str(len(records))}.')

    options = prepare_parsing_options(records)

    if PLATFORM == 'linux64':
        display = Display()
        display.start()

    with Pool(processes=processes_count) as pool:
        pool.map(check_sold_status, options)

    if 'display' in locals():
        display.stop()

    logger.warning('Конец проверки статуса «Продан».')


def check_sold_status(options):
    """Checking the offers' status.

    Args:
        options (dict): The dictionary including `wire_options` and `offers_data` keys.
    """

    wire_options = options['wire_options']
    offers_data = options['offers_data']

    selenium_driver = SeleniumDriver()
    selenium_driver.init_driver(wire_options)

    connection = db_connect()
    cursor = connection.cursor()

    for offer_data in offers_data:
        check_offer_status(offer_data, connection, cursor, selenium_driver)

    cursor.close()
    connection.close()
    selenium_driver.quit()


def check_offer_status(offer_data, connection, cursor, selenium_driver):
    """Checking the single offer's status.

    Args:
        connection (mariadb.connection): The instance of 'mariadb.connection' class.
        cursor (mariadb.connection.cursor): The instance of 'mariadb.connection.cursor' class.
        offer_data (tuple): The tuple with offer's data
        selenium_driver (class 'selenium_driver.SeleniumDriver'): The instance of 'selenium_driver.SeleniumDriver' class
    """

    offer_data = list(offer_data)
    offer_id = offer_data[0]
    url = offer_data[1]
    old_price = offer_data[2]

    logger.info(
        f'Получаем информацию у объявления с id: {str(offer_id)} и url: {url}...')

    try:
        page_source_code = selenium_driver.get_page_source(url)
        scrapping_sleep(from_period=1, to_period=2)
    except Exception as e:
        logger.warning(
            f'Во время получения исходного кода для объявления с id {str(offer_id)} и url {url} возникла ошибка: {str(e)}')
        return

    soup = BeautifulSoup(page_source_code, 'html.parser')
    listing_container_element = soup.find(class_='PageListing')

    if listing_container_element is not None:
        logger.info(
            f'Объявление с id {offer_id} и url {url} заблокировано.')
        return

    sold_container = soup.find(
        class_='CardSold')

    if sold_container is None:
        logger.warning(
            f'Объявление с id {offer_id} и url {url} снова в продаже.')
        data_attributes = soup.find(
            id='sale-data-attributes')

        if data_attributes is not None:
            data_attributes = data_attributes.get('data-bem')
            data_attributes = json.loads(data_attributes)

            if 'price' in data_attributes['sale-data-attributes']:
                price = int(
                    data_attributes['sale-data-attributes']['price'])
                logger.info(
                    f'Цена объявления с id: {offer_id}={str(price)}')
                cursor = connection.cursor()
                sql = '''
                    SELECT
                        `price`
                    FROM
                        `offers_tracking`
                    WHERE
                        `price` > 0 AND `item_id` = ''' + str(offer_data[0]) + '''
                    ORDER BY
                        `checkedon` DESC
                    LIMIT 1
                '''

                try:
                    cursor.execute(sql)
                    offer_tracking_data = cursor.fetchone()
                    logger.info(
                        f'Последняя информация об отслеживании: {offer_tracking_data}')

                    if offer_tracking_data is not None and offer_tracking_data[0] != old_price:
                        old_price = offer_tracking_data[0]

                    if price is not None and price != old_price:
                        logger.warning(
                            f'Новая цена объявления с id: {offer_id} отличается от предыдущей цены ({old_price}).')
                        offer_data.append(price)
                        logger.info(
                            f'Новое содержимое информации о предложении: {str(offer_data)}')

                except Exception as e:
                    logger.warning(
                        f'Не удалось получить данные отслеживания для id {offer_id}. Текст ошибки: {e}')

        set_offer_data(connection, cursor, offer_data)


def set_offer_data(connection, cursor, offer_data):
    """Setting the offers's data

    Args:
        connection (mariadb.connection): The instance of 'mariadb.connection' class.
        cursor (mariadb.connection.cursor): The instance of 'mariadb.connection.cursor' class.
        offer_data (list): The list of offer's data
    """
    STATUS = 'For_sale_again'

    now = datetime.datetime.now()
    sql = '''
        UPDATE `offers_list`
        SET
            `checkedon` = %s,
            `status` = NULL
        WHERE
            `id` = %s
    '''

    try:
        cursor.execute(sql, (now, offer_data[0]))
        connection.commit()
    except Exception as e:
        connection.rollback()
        logger.warning(
            f'Не удалось присвоить объявлению статус «Продается». Текст ошибки: {e}')

    try:
        sql = '''
            INSERT INTO
                `offers_tracking`
                (item_id, checkedon, price, status)
            VALUES
                (?, ?, ?, ?)
        '''

        try:
            cursor.execute(sql, (offer_data[0], now, offer_data[3], STATUS))
            connection.commit()
            logger.warning(
                f'Информация об обновлении статуса для предложения с id: {str(offer_data[0])} успешно добавлена!')
        except Exception as e:
            connection.rollback()
            logger.warning(
                f'Не удалось добавить информацию об изменении статуса для объявления с id: {str(offer_data[0])}. Текст ошибки: {e}')

    except IndexError:
        sql = '''
            INSERT INTO
                `offers_tracking`
                (item_id, checkedon, status)
            VALUES
                (?, ?, ?)
        '''

        try:
            cursor.execute(sql, (offer_data[0], now, STATUS))
            connection.commit()
            logger.warning(
                f'Информация об обновлении статуса для предложения с id: {str(offer_data[0])} успешно добавлена!')
        except Exception as e:
            connection.rollback()
            logger.warning(
                f'Не удалось добавить информацию об изменении статуса для объявления с id: {str(offer_data[0])}. Текст ошибки: {str(e)}')


def prepare_parsing_options(offers):
    """Preparing parsing options

    Args:
        offers (list): The list of offers' data.

    Returns:
        list: The list of options including `wire_options` key.
    """

    proxy_cycle = cycle(AUTO_RU_CHECK_SOLD_PROXIES)
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


if __name__ == '__main__':
    check_sold_offers()
