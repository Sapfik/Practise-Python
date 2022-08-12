import os
from platform_config import PLATFORM

EMAIL_ADDR_FROM = 'root@367423-cc78716.tmweb.ru'
EMAIL_ADDR_TO = [
    'bulatovdm@yandex.ru'
]

ROOT_PATH = os.path.dirname(os.path.abspath(
    os.path.join(os.path.dirname(__file__))))
LOGFILE_PATH = ROOT_PATH + '/scrapper.log'
DRIVER_PATH = f'../webdrivers/{PLATFORM}/chromedriver'
SCRAPPING_SOURCES = {
    'AUTO_RU': 'auto.ru'
}
AUTO_RU_ERROR_PAGE_URL = 'https://auto.ru/sankt-peterburg/sold/'
AUTO_RU_REGIONS_ALIASES = {
    'Санкт-Петербург': 'sankt-peterburg',
    'Москва': 'moskva'
}
AUTO_RU_COOKIES = {
    'name': 'gradius',
    'value': '50'
}
OFFERS_SCRAPPER_PROCESSES_COUNT = 3
SCRAPE_DATA_PROCESSES_COUNT = 1
CHECK_STATUS_PROCESSES_COUNT = 3
CHECK_SOLD_PROCESSES_COUNT = 2

START_YEAR = 2000
SEARCH_PARAMS = [
    'sort=cr_date-desc',
    'top_days=1'
]
SELENIUM_WIRE_OPTIONS = {
    'backend': 'mitmproxy',
    'mitm_http2': False,
    'disable_capture': True,
    'verify_ssl': True,
    'connection_keep_alive': False,
    'max_threads': 3,
    'connection_timeout': None,
}
OFFER_CHECK_DUPLICATES_COLUMNS = [
    'id',
    'url',
    'title',
    'brand',
    'model',
    'release_year',
    'hand_drive',
    'engine_type',
    'engine_volume',
    'power',
    'transmission',
    'body',
    'drive',
    'run',
    'color',
    'status',
    'createdon'
]
DUPLICATES_RUN_DELTA = 200
FOR_SALE_AGAIN_CHECK_DAYS = 30

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
}
LEXICON = {
    'seller_type': {
        'dealer': 'Дилер',
        'private_person': 'Частное лицо'
    },
    'configuration': {
        'label': 'Комплектация',
        'values': {
            'undefined': 'Не известна',
        }
    }
}
