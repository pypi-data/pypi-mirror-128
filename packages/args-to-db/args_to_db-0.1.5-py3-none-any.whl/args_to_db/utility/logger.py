import logging
import sys
from typing import Any, Callable


def init_logging() -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)


def get_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    # logger.setLevel(logging.DEBUG)  # TODO: default logging level
    logger.setLevel(logging.ERROR)
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)
    # console_formatter = logging.Formatter(
    #     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    # )
    # console_handler.setFormatter(console_formatter)
    # add_logging_handler_once(logger, console_handler)

    return logger


def arg_to_str(arg: Any) -> str:
    if isinstance(arg, str):
        return f'\'{arg}\''
    return str(arg)


def function_head_to_str(func: Callable[[Any], Any],
                         *args: Any,
                         **kwargs: Any) -> str:
    args_str = [arg_to_str(arg) for arg in args] + \
               [k + '=' + arg_to_str(v) for k, v in kwargs.items()]
    return func.__name__ + f"({', '.join(args_str)})"


def logged(logger: logging.Logger, level=logging.DEBUG):
    def decorator(function):
        def logged_function(*args, **kwargs):
            logger.log(level, function_head_to_str(function, *args, **kwargs))
            return function(*args, **kwargs)
        return logged_function
    return decorator
