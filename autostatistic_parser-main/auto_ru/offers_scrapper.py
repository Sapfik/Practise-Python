import sys
from pprint import pprint
import re
import datetime
from multiprocessing import Pool
from itertools import cycle, chain

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

import logger
from selenium_driver import SeleniumDriver
from sleep import scrapping_sleep
from lists_methods import merge_list_of_lists, slice_list
from string_to_number import string_to_number
from database import db_connect

from platform_config import PLATFORM
from proxies import AUTO_RU_SCRAPPER_PROXIES
from common_config import LOGFILE_PATH, START_YEAR, SCRAPPING_SOURCES, AUTO_RU_REGIONS_ALIASES, SEARCH_PARAMS, SELENIUM_WIRE_OPTIONS, AUTO_RU_ERROR_PAGE_URL, AUTO_RU_COOKIES, OFFERS_SCRAPPER_PROCESSES_COUNT

logger = logger.get_logger(__name__, LOGFILE_PATH)
start_time = datetime.datetime.now()
processes_count = OFFERS_SCRAPPER_PROCESSES_COUNT


def scrape_offers(region='Санкт-Петербург'):
    """Scrapping offers from a listing.

    Args:
        region (string, optional): The region to parse data. Defaults to "Санкт-Петербург"
    """

    parsing_options = prepare_base_page_parsing_options()

    options = list(map(lambda x: {
        'wire_options': x['wire_options'],
        'region': region,
        'years': x['years']
    }, parsing_options))

    if PLATFORM == 'linux64':
        display = Display()
        display.start()

    with Pool(processes=processes_count) as pool:
        results = pool.map(get_base_pages_data, options)
        pool.close()
        pool.join()

    page_sources = get_pages_sources(results)

    offers_data = []

    for source_code in page_sources:
        page_offers_data = get_offers_data(source_code, region)

        if len(page_offers_data) == 0:
            logger.warning('Отсутствуют предложения для страницы.')
            continue

        offers_data = offers_data + page_offers_data

    logger.warning(
        f'Всего предложений: {len(offers_data)} шт.')

    offers_data = filter_existing_offers(offers_data)
    add_offers_to_db(offers_data)

    logger.warning(
        f'Время выполнения скрипта: {datetime.datetime.now() - start_time}')

    if 'display' in locals():
        display.stop()


def get_pages_sources(data_list):
    """Getting pages sources

    Args:
        data_list (list): The list of dictionaries with `page_sources` and `pagination_urls` keys.

    Returns:
        list: The list of pages' source code.
    """
    page_sources = []
    pagination_urls = []

    for data in data_list:
        page_sources.append(data['page_sources'])

        if 'pagination_urls' in data:
            pagination_urls += data['pagination_urls']

    pagination_urls = merge_list_of_lists(pagination_urls)
    page_sources = merge_list_of_lists(page_sources)

    if len(pagination_urls) > 0:
        logger.warning(
            f'Всего страниц пагинации для всех базовых страниц: {len(pagination_urls)}')
        options = prepare_listing_page_parsing_options(pagination_urls)

        with Pool(processes=processes_count) as pool:
            pagination_page_source = pool.map(get_listing_page_source, options)
            pool.close()
            pool.join()

        pagination_page_source = merge_list_of_lists(pagination_page_source)
        page_sources += pagination_page_source

    return page_sources


def get_base_pages_data(options):
    """Parsing the list of pagination URLs and the base page's source code.

    Args:
        options (dict): The options dictionary including `wire_options` key and `region` key.

    Returns:
        dict: The dictionary with pagination urls and base page's source code.
    """

    wire_options = options['wire_options']
    region = options['region']
    years = options['years']

    region_alias = AUTO_RU_REGIONS_ALIASES[region]

    selenium_driver = SeleniumDriver(cookie_page_url=AUTO_RU_ERROR_PAGE_URL)
    selenium_driver.init_driver(wire_options)
    selenium_driver.set_cookies(AUTO_RU_COOKIES)

    output = {
        'page_sources': [],
        'pagination_urls': []
    }

    for year in years:
        logger.warning(f'Параметры: год – {year}, регион - {region}')
        url = f'https://auto.ru/{region_alias}/cars/{year}-year/used/?{"&".join(SEARCH_PARAMS)}'
        logger.warning(
            f'Получаем исходный код для базовой страницы c url {url}...')

        base_page_source = selenium_driver.get_page_source(url)
        pages_number = parse_pages_number(base_page_source)
        logger.warning(
            f'Всего страниц пагинации для года {year}: {pages_number}')
        output['page_sources'].append(base_page_source)

        # Getting the pagination pages number - start.
        pagination_urls = []

        for page_number in range(1, pages_number + 1):

            if page_number == 1:
                continue

            pagination_urls.append(
                f'{url}&page={str(page_number)}')

        if len(pagination_urls) > 0:
            output['pagination_urls'].append(pagination_urls)
        # Getting the pagination pages number - end.

        scrapping_sleep()

    selenium_driver.quit()
    return output


def get_listing_page_source(options):
    """Getting the listing page's source code by the URL.

    Args:
        options (dict): The dictionary with `wire_options` and `url` keys.

    Returns:
        list: The list of pages' source code.
    """

    wire_options = options['wire_options']
    urls = options['urls']

    selenium_driver = SeleniumDriver(cookie_page_url=AUTO_RU_ERROR_PAGE_URL)
    selenium_driver.init_driver(wire_options)
    selenium_driver.set_cookies(AUTO_RU_COOKIES)

    page_sources = []

    for url in urls:
        logger.warning(f'Получаем исходный код для страницы с URL {url}')
        page_source = selenium_driver.get_page_source(url)
        page_sources.append(page_source)
        scrapping_sleep()

    selenium_driver.quit()

    return page_sources


def prepare_listing_page_parsing_options(urls):
    """Preparing parsing options
    Args:
        urls (list): The list of listing urls.

    Returns:
        list: The list of options.
    """

    proxy_cycle = cycle(AUTO_RU_SCRAPPER_PROXIES)
    proxy = next(proxy_cycle)

    options = []
    urls_list = slice_list(urls, processes_count)
    options_count = min(len(urls_list), processes_count)

    for i in range(options_count):
        wire_options = SELENIUM_WIRE_OPTIONS.copy()
        wire_options['proxy'] = {
            'https': f'https://{proxy}'
        }
        options.append({
            'wire_options': wire_options,
            'urls': urls_list[i]
        })
        proxy = next(proxy_cycle)

    return options


def prepare_base_page_parsing_options():
    """Preparing parsing options

    Returns:
        list: The list of options including `wire_options` and `year` keys.
    """

    current_year = start_time.year
    year = START_YEAR
    proxy_cycle = cycle(AUTO_RU_SCRAPPER_PROXIES)
    proxy = next(proxy_cycle)

    years = []

    while year <= current_year:
        years.append(year)
        year += 1

    years_list = slice_list(years, processes_count)

    options = []

    options_count = min(len(years_list), processes_count)

    for i in range(options_count):
        wire_options = SELENIUM_WIRE_OPTIONS.copy()
        wire_options['proxy'] = {
            'https': f'https://{proxy}'
        }
        options.append({
            'wire_options': wire_options,
            'years': years_list[i]
        })
        proxy = next(proxy_cycle)

    return options


def parse_pages_number(page_source):
    """Getting the URL's pages number.

    Args:
        page_source (string): The page source code.

    Returns:
        int: The pages number.
    """

    soup = BeautifulSoup(page_source, 'html.parser')
    pages = soup.find_all(class_='ListingPagination__page')
    pages_number = 1

    if pages is not None:
        last_page = None

        for last_page in pages:
            pass

        if last_page:
            pages_number = int(last_page.get_text())

    return pages_number


def get_offers_data(source_code, region):
    """Getting the page offers data

    Args:
        source_code (string): The page source code.
        region (string): The current region.

    Returns:
        list: The list of offers dictionaries.
    """

    soup = BeautifulSoup(source_code, 'html.parser')
    offers_data = []

    offers_listing = soup.find(class_='ListingCars_outputType_list')

    if offers_listing is None:
        return offers_data

    offers_elements = offers_listing.find_all(class_='ListingItem')

    if len(offers_elements) == 0:
        return offers_data

    for offer_element in offers_elements:
        offer_data = {}

        try:
            url_element = offer_element.find(
                'a', class_='ListingItemTitle__link')
        except:
            logger.warning('Отсутствует ссылка для предложения.')
            continue

        try:
            href = url_element.get('href')
        except:
            logger.warning('Отсутствует аттрибут href для предложения.')
            continue

        href = href.split('?')[0]
        offer_data['url'] = href

        title = re.sub(' +', ' ', url_element.get_text())
        offer_data['title'] = title

        id_hash_data = get_id_hash_from_url(href)
        offer_id = id_hash_data['id']
        offer_hash = id_hash_data['hash']

        if offer_id is None or hash is None:
            logger.warning(
                f'Для предложения с url {href} отсутствуют id или hash.')
            continue

        offer_data['id'] = offer_id
        offer_data['hash'] = offer_hash

        price_element = offer_element.find(class_='ListingItem__price')

        if price_element is not None:
            price = price_element.get_text()
            price = string_to_number(price)
            offer_data['price'] = price

        release_year_element = offer_element.find(class_='ListingItem__year')

        if release_year_element is not None:
            release_year = release_year_element.get_text()
            release_year = string_to_number(release_year)
            offer_data['release_year'] = release_year

        run_element = offer_element.find(class_='ListingItem__kmAge')

        if run_element is not None:
            run = run_element.get_text()
            run = string_to_number(run)
            offer_data['run'] = run

        offer_data['createdon'] = datetime.datetime.now()
        offer_data['region'] = region
        offer_data['source'] = SCRAPPING_SOURCES['AUTO_RU']

        offers_data.append(offer_data)

    return offers_data


def filter_existing_offers(data):
    """Filtering the existing in the database offers.

    Args:
        data (list): The list of offers' data.

    Returns:
        list: The filtered list of offers' data.
    """

    sql = '''
        SELECT
            url
        FROM
            offers_list
    ;'''

    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    existing_offers = cursor.fetchall()

    logger.warning(
        f'Количество предложений в базе: {len(existing_offers)}')

    cursor.close()
    connection.close()

    existing_urls = [i[0] for i in existing_offers]
    urls_to_remove = []

    for parsed_offer in data:
        offer_url = parsed_offer['url']

        if offer_url in existing_urls:
            urls_to_remove.append(offer_url)

    data = list(filter(lambda x: x['url'] not in urls_to_remove, data))

    logger.warning(
        f'Количество предложений для добавления в базу: {len(data)}')

    return data


def add_offers_to_db(data):
    """Adding offers to the database.

    Args:
        data (list): The list of offers' data.
    """

    connection = db_connect()
    cursor = connection.cursor()
    added_offers_number = 0

    for offer_data in data:
        offer_id = offer_data['id']
        offer_hash = offer_data['hash']
        url = offer_data['url']
        title = offer_data['title']

        if 'price' in offer_data:
            price = offer_data['price']
        else:
            price = 0

        release_year = offer_data['release_year']
        run = offer_data['run']
        createdon = offer_data['createdon']
        region = offer_data['region']
        source = offer_data['source']

        try:
            cursor.execute(
                '''
                    INSERT INTO
                        offers_list (offer_id, hash, url, title, price,
                                     release_year, run, createdon, region, source)
                    VALUES
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    offer_id,
                    offer_hash,
                    url,
                    title,
                    price,
                    release_year,
                    run,
                    createdon,
                    region,
                    source
                )
            )
            connection.commit()
            logger.warning(f'Добавлено предложение с URL {url}')
            added_offers_number += 1
        except Exception as e:
            logger.warning(
                f'Не удалось добавить в базу предложение в url: {url}. Текст ошибки: {str(e)}')

    cursor.close()
    connection.close()

    if added_offers_number > 0:
        logger.warning(
            f'Добавлено новых предложений в базу: {added_offers_number} шт.')


def get_id_hash_from_url(url):
    """Getting `id` and `hash` values from the url.

    Args:
        url (string): The offer's URL.

    Returns:
        dict: The dictionary with id and hash.
    """

    url_list = url.split('/')
    url_list = list(filter(None, url_list))
    id_hash = url_list[-1].split('-')

    return {
        'id': id_hash[0],
        'hash': id_hash[1]
    }


if __name__ == '__main__':
    scrape_offers()
