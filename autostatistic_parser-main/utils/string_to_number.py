import re
import logger
from common_config import LOGFILE_PATH

logger = logger.get_logger(__name__, LOGFILE_PATH)


def string_to_number(string):
    """Trasform string to number

    Args:
        string (string): The input string.

    Returns:
        int: The output number.
    """
    string = re.sub(r'[^0-9]+', r'', string)

    try:
        int(string)
    except:
        logger.warning(f'Не удается преобразовать строку "{string}" в число.')
        return None
    else:
        return int(string)
