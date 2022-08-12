from database import db_connect


def find_url_duplicated():
    """Finding the URL duplicates.
    """
    connection = db_connect()
    cursor = connection.cursor()

    sql = '''
        SELECT
            offers_list . id
        FROM
            offers_list
        LEFT OUTER JOIN
            (
                SELECT
                    MIN(id) AS id,
                    url
                FROM
                    offers_list
                GROUP BY
                    url
            ) AS tmp
        ON
            offers_list . id = tmp . id
        WHERE
            tmp . id IS NULL

    ;'''

    cursor.execute(sql)
    duplicated_ids = cursor.fetchall()

    cursor.close()
    connection.close()

    with open('docs/duplicated_ids.txt', 'w', encoding='utf-8') as file:
        for dupliated_id in duplicated_ids:
            file.seek(0, 2)
            file.write(f'{str(dupliated_id[0])}\n')


if __name__ == '__main__':
    find_url_duplicated()
