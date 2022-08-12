import re
from logger import get_logger
from database import db_connect
from common_config import LOGFILE_PATH
from transliterate.config import TRANSLITERATION_TABLE

logger = get_logger(__name__, LOGFILE_PATH)


def transliterate_title(connection, cursor, item_title):
    """Transliterate the item's title

    Args:
        connection (mariadb.connection): The instance of 'mariadb.connection' class.
        cursor (mariadb.connection.cursor): The instance of 'mariadb.connection.cursor' class.
        item_title (string): The item's title
    """
    if item_title is None:
        return

    item_title = re.sub(' +', ' ', item_title)
    sql = '''
        SELECT
            title
        FROM
            offers_cards
        WHERE
            title = "''' + str(item_title) + '''";
    '''

    try:
        cursor.execute(sql)
        records = cursor.fetchall()

        if len(records) == 0:
            item_alias = transliterate_string(item_title)

            try:
                cursor.execute(
                    'INSERT INTO offers_cards (title, alias) VALUES (?, ?)',
                    (item_title, item_alias)
                )
                connection.commit()
                logger.info(
                    f'Добавлена карточка для заголовка «{str(item_title)}» с alias: {str(item_alias)}.')
            except:
                connection.rollback()
                logger.warning(
                    f'Не удалось добавить в таблицу `offers_cards` карточку c заголовком «{str(item_title)}»')
        else:
            logger.info(
                f'Карточка для заголовка «{str(item_title)}» уже в базе данных.')

    except Exception as e:
        logger.warning(
            f'Не удалось получить данные о карточке предложения с заголовком «{str(item_title)}». Текст ошибки: {str(e)}.')


def transliterate_string(string):
    """Transliterating string.

    Args:
        string (string): The string to translate.

    Returns:
        string: The transliterated string
    """

    if string is None:
        return None

    string = string.strip()
    string = string.lower()
    string = re.sub(' +', ' ', string)
    string = re.sub(r'[^\w|\s|\.]', '', string)
    string = re.sub(r'(\s|\.)', '-', string)

    transliterated_string = ''

    for letter in string:

        if letter in TRANSLITERATION_TABLE:
            transliterated_string = transliterated_string + \
                TRANSLITERATION_TABLE[letter]
        else:
            transliterated_string = transliterated_string + letter

    return transliterated_string
