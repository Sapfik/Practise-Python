import datetime
from logger import get_logger
from database import db_connect
from common_config import LOGFILE_PATH, OFFER_CHECK_DUPLICATES_COLUMNS, DUPLICATES_RUN_DELTA

logger = get_logger(__name__, LOGFILE_PATH)


def find_duplicates(cursor, offer_id):
    """Finding duplicates for an offer with the specified id.

    Args:
        cursor (mariadb.connection.cursor): The instance of 'mariadb.connection.cursor' class.
        offer_id (int): The offer' id.

    Returns:
        dict: The dictionaty with lists of ids and their data.
    """

    if offer_id is not None:
        sql = '''
            SELECT ''' + str(','.join(OFFER_CHECK_DUPLICATES_COLUMNS)) + '''
            FROM
                offers_list
            WHERE id = ''' + str(offer_id) + ''';
        '''
    else:
        sql = '''
            SELECT
                ''' + str(','.join(OFFER_CHECK_DUPLICATES_COLUMNS)) + '''
            FROM offers_list
            ORDER BY
                id DESC
            LIMIT 2000'''

    try:
        cursor.execute(sql)
        offers = cursor.fetchall()

        if len(offers) == 0:
            logger.warning('Отсутствуют объявления для поиска дубликатов')
            return None

        duplicates_ids = []
        duplicates_data = []

        for offer in offers:

            if offer[0] in duplicates_ids:
                continue

            duplicates = check_duplicates(cursor, offer)

            if duplicates is not False and duplicates is not None:
                duplicates.append(offer)
                earliest_offer = min(duplicates, key=return_first_element)
                duplicates_ids.append(earliest_offer[0])
                item = {}
                item['id'] = earliest_offer[0]
                item['url'] = earliest_offer[1]
                item['Статус'] = 'Опубликован впервые'
                duplicates_data.append(item)

                for duplicate in duplicates:

                    if duplicate[0] == earliest_offer[0]:
                        continue

                    duplicates_ids.append(duplicate[0])
                    item = {}
                    item['id'] = duplicate[0]
                    item['url'] = duplicate[1]
                    item['Статус'] = 'Дубль'
                    item['id опубликованного впервые'] = earliest_offer[0]
                    item['url опубликованного впервые'] = earliest_offer[1]
                    duplicates_data.append(item)

        output = {
            'ids': duplicates_ids,
            'data': duplicates_data
        }

        return output
    except Exception as e:
        logger.warning(
            f'Не удалось выбрать объявления для поиска дубликатов. Текст ошибки: {str(e)}')
        return None


def check_duplicates(cursor, offer):
    """Checking duplicates for the offer

    Args:
        cursor (mariadb.connection.cursor): The instance of 'mariadb.connection.cursor' class.
        offer (tuple): The tuple with the offer' data.

    Returns:
        list: The list of duplicates
    """

    where = []
    logger.info(f'Проверяем предложение с id: {str(offer[0])} на дубли.')

    for index, column in enumerate(OFFER_CHECK_DUPLICATES_COLUMNS):

        if column == 'status':
            continue
        if column == 'createdon':
            continue

        if offer[index] is not None:

            if column == 'id':
                condition = column + ' != ' + str(offer[index])
            elif column == 'url':
                condition = column + ' != "' + str(offer[index]) + '"'
            elif column == 'run':
                run_from = int(offer[index]) - DUPLICATES_RUN_DELTA
                run_from = max(run_from, 0)

                run_to = int(offer[index]) + DUPLICATES_RUN_DELTA

                condition = column + ' >= ' + \
                    str(run_from) + ' AND ' + column + ' <= ' + str(run_to)
            else:

                if isinstance(offer[index], (int)):
                    condition = column + ' = ' + str(offer[index])
                elif isinstance(offer[index], (float)):
                    condition = 'CAST(' + str(column) + ' AS DECIMAL) = CAST(' + \
                        str(offer[index]) + ' AS DECIMAL)'
                else:
                    condition = column + ' = "' + str(offer[index]) + '"'

        else:
            condition = column + ' IS NULL'

        where.append(' ' + condition)

    where.append(' (checkedon BETWEEN "' +
                 str(offer[16] - datetime.timedelta(days=30)) + '" AND "' + str(offer[16]) + '")')
    where.append(' status = "Sold"')

    sql = '''
        SELECT
            ''' + str(','.join(OFFER_CHECK_DUPLICATES_COLUMNS)) + '''
        FROM
            offers_list
        WHERE
            ''' + ('\n AND').join(where) + ''';
    '''

    try:
        cursor.execute(sql)
        offers = cursor.fetchall()

        logger.info(f'Количество предложений для сравнения {str(len(offers))}')

        if len(offers) > 0:
            return offers

        return False

    except Exception as e:
        logger.warning(
            f'Не удалось выполнить запрос для поиска дубликатов для предложения с id: {str(offer[0])}. Текст ошибки: {str(e)}')
        return False


def add_duplicates_to_base(connection, cursor, duplicated_ids):
    """Adding duplicates info to the database.

    Args:
        connection (mariadb.connection): The instance of 'mariadb.connection' class.
        cursor (mariadb.connection.cursor): The instance of 'mariadb.connection.cursor' class.
        duplicated_ids (list): The list of duplicated ids.
    """

    for duplicated_id in duplicated_ids:

        sql = '''
            UPDATE offers_list
            SET duplicated = %s
            WHERE id = %s
        '''

        try:
            cursor.execute(sql, (1, duplicated_id))
            connection.commit()
            logger.warning(f'Найден дубль с id {str(duplicated_id)}')
        except Exception as e:
            connection.rollback()
            logger.warning(
                f'Не удалось добавить информации о том, что объявление с id = {str(duplicated_id)} является дублем\nОшибка: {str(e)}')

        for duplicated_related in duplicated_ids:

            if duplicated_related != duplicated_id:
                sql = '''
                    INSERT INTO offers_duplicates
                        (item_id, related_id)
                    VALUES
                        (?,?)
                '''

                try:
                    cursor.execute(sql, (duplicated_id, duplicated_related))
                    connection.commit()
                    logger.warning(
                        f'Добавлена новая запись в таблицу с дублями для пары {str(duplicated_id)} и {str(duplicated_related)}')
                except Exception as e:
                    connection.rollback()
                    logger.warning(
                        f'Не удалось добавить новую запись в таблицу с дублями для пары {str(duplicated_id)} и {str(duplicated_related)}\nОшибка: {str(e)}')


def return_first_element(input_list):
    """Getting the first element of the input list.

    Args:
        list (list): The input list.

    Returns:
        mixed: The first list's element.
    """
    return input_list[0]
