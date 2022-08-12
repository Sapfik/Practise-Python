import sys
import datetime
import json
from pprint import pprint
from multiprocessing import Pool
from itertools import cycle

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

from logger import get_logger
from selenium_driver import SeleniumDriver
from database import db_connect
from sleep import scrapping_sleep
from lists_methods import slice_list

from common_config import LOGFILE_PATH, SELENIUM_WIRE_OPTIONS, CHECK_STATUS_PROCESSES_COUNT, LEXICON
from proxies import AUTO_RU_OFFER_SCRAPE_DATA_PROXIES
from platform_config import PLATFORM

logger = get_logger(__name__, LOGFILE_PATH)
processes_count = CHECK_STATUS_PROCESSES_COUNT


def check_offers_data(region='Санкт-Петербург'):
    """Checking the offers status.

    Args:
        region (string, optional): The region to check data. Defaults to "Санкт-Петербург"
    """

    logger.warning(f'Начинаем проверку статуса объявлений...')

    if PLATFORM == 'linux64':
        display = Display()
        display.start()

    offers = get_in_sale_offers(region)
    options = prepare_parsing_options(offers)

    with Pool(processes=processes_count) as pool:
        pool.map(check_offers, options)
        pool.close()
        pool.join()

    if 'display' in locals():
        display.stop()


def check_offer(offer_data, selenium_driver, connection, cursor):
    """Checking the offer's price and status.

    Args:
        offer_data (dict): [description]
        selenium_driver (class 'selenium_driver.SeleniumDriver'): The instance of 'selenium_driver.SeleniumDriver' class
        connection (mariadb.connection): The instance of 'mariadb.connection' class.
        cursor (mariadb.connection.cursor): The instance of 'mariadb.connection.cursor' class.
    """

    offer_id = offer_data['id']
    url = offer_data['url']
    createdon = offer_data['createdon']
    checkedon = offer_data['checkedon']
    inspections_number = offer_data['inspections_number']
    old_price = offer_data['old_price']
    old_configuration = offer_data['configuration']
    tracking_price = offer_data['tracking_price']

    if tracking_price:
        old_price = tracking_price

    logger.warning(f'Проверяем объявление в id {offer_id}...')

    now = datetime.datetime.now()

    if inspections_number == 0:
        if createdon < now - datetime.timedelta(hours=1):
            pass
        else:
            return

    elif inspections_number == 1:
        if createdon < now - datetime.timedelta(hours=2):
            pass
        else:
            return

    elif inspections_number == 2:
        if createdon < now - datetime.timedelta(hours=3):
            pass
        else:
            return

    elif inspections_number == 3:
        if now > datetime.datetime(createdon.year, createdon.month, createdon.day) + datetime.timedelta(hours=23):
            pass
        else:
            return

    elif inspections_number == 4:
        if now > datetime.datetime(createdon.year, createdon.month, createdon.day) + datetime.timedelta(days=1, hours=10):
            pass
        else:
            return

    elif inspections_number == 5:
        if now > datetime.datetime(createdon.year, createdon.month, createdon.day) + datetime.timedelta(days=1, hours=14):
            pass
        else:
            return

    elif inspections_number == 6:
        if now > datetime.datetime(createdon.year, createdon.month, createdon.day) + datetime.timedelta(days=1, hours=23):
            pass
        else:
            return

    else:
        if now > datetime.datetime(checkedon.year, checkedon.month, checkedon.day) + datetime.timedelta(days=1, hours=23):
            pass
        else:
            return

    try:
        page_source_code = selenium_driver.get_page_source(url)
        scrapping_sleep(from_period=1, to_period=2)
    except Exception as e:
        logger.warning(
            f'Во время получения исходного кода для объявления с id {str(offer_id)} и url {url} возникла ошибка: {str(e)}')
        return

    inspections_number += 1
    soup = BeautifulSoup(page_source_code, 'html.parser')

    listing_container_element = soup.find(class_='PageListing')

    if listing_container_element is not None:
        status = 'Blocked'
        sql = '''
            UPDATE
                offers_list
            SET
                checkedon = %s,
                status = %s,
                inspections_number = %s
            WHERE
                id = %s;
        '''

        try:
            cursor.execute(
                sql, (now, status, inspections_number, offer_id))
            connection.commit()
        except Exception as e:
            connection.rollback()
            logger.warning(
                f'Не удалось добавить дату изменения для предложения с id {str(offer_id)}\nОшибка: {str(e)}')
            return

        sql = '''
            INSERT INTO
                offers_tracking (item_id, checkedon, status)
            VALUES
                (?, ?, ?);
        '''

        try:
            cursor.execute(sql, (offer_id, now, status))
            connection.commit()
        except Exception as e:
            connection.rollback()
            logger.warning(
                f'Не удалось добавить информацию об изменении статуса для предложения с id {str(offer_id)}\nОшибка: {str(e)}')
        return

    check_configuration(soup, old_configuration,
                        offer_id, url, connection, cursor)

    sold_container = soup.find(class_='CardSold')

    if sold_container is not None:
        status = 'Sold'
        sold_time_container = soup.find(class_='CardSold__time')

        if sold_time_container is not None:
            sold_time = sold_time_container.find(class_='CardSold__title')

            if sold_time is not None:
                sold_time = sold_time.get_text().strip()
                sql = '''
                        UPDATE
                            offers_list
                        SET
                            status = %s,
                            sale_time = %s,
                            checkedon = %s,
                            inspections_number = %s
                        WHERE
                            id = %s;
                '''

                try:
                    cursor.execute(
                        sql, (status, sold_time, now, inspections_number, offer_id))
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    logger.warning(
                        f'Не удалось добавить время продажи и статус для предложения с id {str(offer_id)}\nОшибка: {str(e)}')
                    return

                sql = '''
                    INSERT INTO
                        offers_tracking (item_id, checkedon, status)
                        VALUES
                            (?, ?, ?);
                '''

                try:
                    cursor.execute(sql, (offer_id, now, status))
                    connection.commit()
                except Exception as e:
                    connection.rollback()
                    logger.warning(
                        f'Не удалось добавить информацию об изменении статуса для предложения с id {str(offer_id)}\nОшибка: {str(e)}')
                return

        else:
            sql = '''
                UPDATE
                    offers_list
                SET
                    status = %s,
                    checkedon = %s,
                    inspections_number = %s
                WHERE
                    id = %s;
            '''

            try:
                cursor.execute(
                    sql, (status, now, inspections_number, offer_id))
                connection.commit()
            except Exception as e:
                connection.rollback()
                logger.warning(
                    f'Не удалось добавить статус для предложения с id {str(offer_id)}\nОшибка: {str(e)}')
                return

            sql = '''
                INSERT INTO
                    offers_tracking (item_id, checkedon, status)
                VALUES
                    (?, ?, ?);
            '''

            try:
                cursor.execute(sql, (offer_id, now, status))
                connection.commit()
            except Exception as e:
                connection.rollback()
                logger.warning(
                    f'Не удалось добавить информацию об изменении статуса для предложения с id {str(offer_id)}\nОшибка: {str(e)}')
            return

    else:
        sql = '''
            UPDATE
                offers_list
            SET
                checkedon = %s,
                inspections_number = %s
            WHERE
                id = %s
        '''

        try:
            cursor.execute(sql, (now, inspections_number, offer_id))
            connection.commit()
        except Exception as e:
            connection.rollback()
            logger.warning(
                f'Не удалось добавить время продажи и статус для предложения с id {str(offer_id)}\nОшибка: {str(e)}')
            return

        data_attributes = soup.find(id='sale-data-attributes')

        if data_attributes is not None:
            data_attributes = data_attributes.get('data-bem')
            data_attributes = json.loads(data_attributes)

            if 'price' in data_attributes['sale-data-attributes']:
                price = int(
                    data_attributes['sale-data-attributes']['price'])

                if old_price != price:
                    sql = '''
                        INSERT INTO
                            offers_tracking (item_id, checkedon, price)
                        VALUES (?, ?, ?);
                    '''

                    try:
                        cursor.execute(sql, (offer_id, now, price))
                        connection.commit()
                    except Exception as e:
                        connection.rollback()
                        logger.warning(
                            f'Не удалось добавить информацию об изменении цены для предложения с id {str(offer_id)}\nОшибка: {str(e)}')
                    return

        else:
            logger.warning(
                f'У предложения с id {str(offer_id)} нет информации о цене.')


def check_offers(options):
    """Checking the offer status and price.

    Args:
        options (dict): The dictionary with options.
    """

    wire_options = options['wire_options']

    selenium_driver = SeleniumDriver()
    selenium_driver.init_driver(wire_options)

    offers_data = options['offers_data']

    connection = db_connect()
    cursor = connection.cursor()

    for offer_data in offers_data:
        check_offer(offer_data, selenium_driver, connection, cursor)

    cursor.close()
    connection.close()
    selenium_driver.quit()


def check_configuration(soup, old_configuration, offer_id, url, connection, cursor):
    """Checking the configuration for the offer.

    Args:
        soup (class 'bs4.BeautifulSoup'): The instance of 'bs4.BeautifulSoup'
        old_configuration (str): The old offer's configuration.
        offer_id (int): The offer's id.
        url (str): The offer's URL.
        connection (mariadb.connection): The instance of 'mariadb.connection' class.
        cursor (mariadb.connection.cursor): The instance of 'mariadb.connection.cursor' class.
    """

    configuration_title = soup.find(
        class_='CardComplectation__title')

    if configuration_title is not None:
        configuration_text = configuration_title.get_text().replace(
            LEXICON['configuration']['label'], '').strip()

        if configuration_text == '':
            configuration_value = LEXICON['configuration']['values']['undefined']
        else:
            configuration_value = configuration_text
    else:
        configuration_value = None

    if old_configuration != configuration_value:
        sql = '''
            UPDATE `offers_list`
            SET `configuration` = %s
            WHERE id = %s
        '''

        try:
            cursor.execute(sql, (configuration_value, offer_id))
            connection.commit()
            logger.info(
                f'Обновили комплектацию для предложения с id {str(offer_id)} и url: {url}')
        except Exception as e:
            connection.rollback()
            logger.warning(
                f'Не удалось изменить комплектацию для предложения с id {str(offer_id)}\nОшибка: {str(e)}')
    else:
        logger.info(
            f'Комплектация для предложения с id {str(offer_id)} и url {url} осталась прежней.')


def prepare_parsing_options(offers):
    """Preparing parsing options.

    Args:
        offers (list): The list of offers' data.

    Returns:
        (list): The list of options.
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


def get_in_sale_offers(region='Санкт-Петербург'):
    """Getting the offers in sale.

    Args:
        region (str, optional): The city for filter offers. Defaults to 'Санкт-Петербург'.

    Returns:
        list: The list of tuples with offers' data.
    """

    connection = db_connect()
    cursor = connection.cursor()

    sql = '''
        SELECT
            `offer` . `id`,
            `offer` . `url`,
            `offer` . `price`,
            `offer` . `createdon`,
            `offer` . `checkedon`,
            `offer` . `inspections_number`,
            `offer` . `configuration`,
            `tracking` . `price` AS `tracking_price`
        FROM
            `offers_list` AS `offer`
        LEFT JOIN
            `offers_tracking` AS `tracking`
        ON
            `tracking` . `item_id` = `offer` . `id` AND
            `tracking` . `checkedon` = (
                (
                SELECT
                    MAX(`inner_tracking` . `checkedon`)
                FROM
                    `offers_tracking` AS `inner_tracking`
                WHERE
                    `inner_tracking` . `item_id` = `offer` . `id`
                )
            )
        WHERE
            `offer` . `url` IS NOT NULL AND
            `offer` . `status` IS NULL AND
            `offer` . `region` = "''' + region + '''"
        ORDER BY
            `offer` . `id` DESC,
            `tracking` . `checkedon` DESC;
    '''
    offers = []

    try:
        cursor.execute(sql)
        offers = cursor.fetchall()
        logger.warning(
            f'Количество объявлений для проверки статуса: {len(offers)}')
    except Exception as e:
        logger.warning(
            f'Во время выборки объявлений для проверки статуса произошла ошбика. Текст ошибки: {str(e)}')

    cursor.close()
    connection.close()

    offers = list(map(lambda x: {
        'id': x[0],
        'url': x[1],
        'old_price': x[2],
        'createdon': x[3],
        'checkedon': x[4],
        'inspections_number': x[5],
        'configuration': x[6],
        'tracking_price': x[7]
    }, offers))

    return offers


if __name__ == '__main__':
    check_offers_data()
