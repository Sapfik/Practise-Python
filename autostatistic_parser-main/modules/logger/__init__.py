import logging

_log_format = f'%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'


def get_file_handler(logfile):
    """Getting the file handler.

    Args:
        logfile (string): The path to the log file.

    Returns:
        logging.FileHandler: The instance of the `logging.FileHandler` class.
    """

    if logfile == '':
        logfile = 'scrapper.log'

    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    """Getting the stream handler.

    Returns:
        logging.StreamHandler: The instance of the `logging.StreamHandler` class.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name, logfile=''):
    """Getting the logger.

    Args:
        name (string): The logger's name.
        logfile (string): The path to the log file.

    Returns:
        logging.Logger: The instance of the `logging.Logger` class.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler(logfile))
    logger.addHandler(get_stream_handler())
    return logger
