# coding=utf-8
from typing import Callable, Dict, Any


def retryable(fun: Callable[[Any], None], re_init_func: Callable[[], Any], max_tries: int, *args: Dict[str, Any]):
    """
    Retries the function multiple times, based on the max_tries
    :param max_tries:
        max number of tries
    :type max_tries: ``int``
    :param fun:
        main function to retry
    :type fun: ``Callable[[...], None]``
    :param re_init_func:
        function to run after exception is raised
    :type re_init_func: ``Callable``
    :param args:
        main function arguments
    """
    for _ in range(max_tries):
        try:
            fun(*args)
            break
        except (ValueError, Exception):
            re_init_func()
            continue
