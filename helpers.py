"""Helper functions for AdventOfCode"""
import requests
import logging
from time import perf_counter

# Session cookie is valid for 10 years!
COOKIEFILE = ".session_cookie"
level = logging.INFO
fmt = "[%(levelname)s] %(asctime)s - %(message)s"
logging.basicConfig(level=level, format=fmt)


def read_url(url: str) -> str:
    """Get the unmolested data from a URL"""

    def read_cookie(file: str) -> str:
        """Get the AdventOfCode session cookie we saved earlier"""
        with open(file, mode="r") as f:
            return f.read().strip()

    session_cookie = {"session": read_cookie(COOKIEFILE)}
    with requests.get(url=url, timeout=5, cookies=session_cookie) as content:
        return content.text


def timethis(func):
    """Sample decorator to report a function runtime in milliseconds"""

    def wrapper(*args, **kwargs):
        # Make sure we accept any number of args / keyword args
        time_before = perf_counter()
        retval = func(*args, **kwargs)
        time_after = perf_counter()
        time_diff = time_after - time_before
        # __qualname__ returns the name of the func passed in
        logging.info(f"({func.__qualname__}) took {time_diff*1000:.4f} msec")
        return retval

    return wrapper
