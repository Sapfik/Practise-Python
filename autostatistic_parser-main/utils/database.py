import sys
import mariadb
import logger
from platform_config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from common_config import LOGFILE_PATH

logger = logger.get_logger(__name__, LOGFILE_PATH)


def db_connect():
    """Getting the MariaDB connection's instance

    Returns:
        'mariadb.connection': The instance of 'mariadb.connection' class.
    """
    try:
        mariadb_connection = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
    except mariadb.Error as e:
        logger.error(f'Error connecting to MariaDB Platform: {str(e)}')
        sys.exit(1)

    return mariadb_connection
