from pprint import pprint
from multiprocessing import Pool
from itertools import cycle
from logger import get_logger
from proxies import AUTO_RU_SCRAPPER_PROXIES
from common_config import LOGFILE_PATH, SELENIUM_WIRE_OPTIONS
from selenium_driver import SeleniumDriver

logger = get_logger(__name__, LOGFILE_PATH)

PROXIES_TO_TEST = [
    'BDh2ry:zeTkirAwnR@46.8.15.33:1050',
    'BDh2ry:zeTkirAwnR@46.8.57.52:1050',
]


def main():
    """Testing the proxies.
    """

    parsing_options = prepare_parsing_options()

    with Pool(processes=len(PROXIES_TO_TEST)) as pool:
        results = pool.map(get_pages_source_codes, parsing_options)
        pool.close()
        pool.join()

    pprint(results)


def get_pages_source_codes(options):
    """Getting the pages' source codes

    Args:
        options (dict): The dictionary of options.

    Returns:
        str: The page's source code.
    """

    url = 'http://icanhazip.com/'
    logger.info(
        f'Получаем исходный код для url {url} и прокси {options["proxy"]}')

    selenium_driver = SeleniumDriver()
    selenium_driver.init_driver(options)
    source_code = selenium_driver.get_page_source(url)
    return source_code


def prepare_parsing_options():
    """Preparing parsing options.

    Returns:
        list: The list of options.
    """

    proxy_cycle = cycle(PROXIES_TO_TEST)
    proxy = next(proxy_cycle)
    options = []

    i = 0

    while i < len(PROXIES_TO_TEST):
        proxy = next(proxy_cycle)
        wire_options = SELENIUM_WIRE_OPTIONS.copy()
        wire_options['proxy'] = {
            'https': f'https://{proxy}'
        }

        options.append(wire_options)
        i += 1

    return options


if __name__ == '__main__':
    main()
