import time
import random


def scrapping_sleep(from_period=2, to_period=3):
    """Sleeping the random perion of time.

    Args:
        from (int): The botton border (seconds).
        to (int): The upper border (seconds).
    """
    time.sleep(random.randint(from_period, to_period))
