"""
Модуль определения системного логгера
Автор Денис Шелемех, 2021
"""

import logging
from functools import wraps
from typing import Any, Tuple, Dict

from engine.config import config


class Logger:
    """
    Класс логгера. Синглтон
    """
    # кол-во экземпляров класса
    instances = 0

    @classmethod
    def init(cls) -> None:
        """
        Метод гарантирует конструирование класса в качестве синглтона
        Используется методом __init__()

        Аргументы
        cls - класс (объект)
        """
        if cls.instances > 0:
            raise RuntimeError(cls.__name__ + " is a singleton class")
        else:
            cls.instances += 1

    def __init__(self) -> None:
        Logger.init()
        self._log_file_name = None
        self._log_format = None
        self._log_level = None

        self._log_file_name = config["LOGGING"]["LOG_FILE_NAME"]
        self._log_format = ' %(asctime)s - %(levelname)s - %(message)s '
        self._log_level = eval(config["LOGGING"]["LOG_LEVEL"])

        logging.basicConfig(filename=self.log_file_name,
                            format=self.log_format,
                            level=self.log_level)

        self._logger = logging.getLogger(__name__)

    @property
    def log_file_name(self) -> str:
        return self._log_file_name

    @property
    def log_format(self) -> str:
        return self._log_format

    @property
    def log_level(self) -> int:
        return self._log_level

    @log_level.setter
    def log_level(self, value: int) -> None:
        self._logger.level = value

    def debug(self, msg: str, *args: Tuple, **kwargs: Dict) -> None:
        self._logger.debug(msg=msg, *args, **kwargs)

    def info(self, msg: str, *args: Tuple, **kwargs: Dict) -> None:
        self._logger.info(msg=msg, *args, **kwargs)

    def warning(self, msg: str, *args: Tuple, **kwargs: Dict) -> None:
        self._logger.warning(msg=msg, *args, **kwargs)

    def error(self, msg: str, *args: Tuple, **kwargs: Dict) -> None:
        self._logger.error(msg=msg, *args, **kwargs)

    def critical(self, msg: str, *args: Tuple, **kwargs: Dict) -> None:
        self._logger.critical(msg=msg, *args, **kwargs)

    @staticmethod
    def form_string_from_args(func, *args: Tuple, **kwargs: Dict) -> str:
        """
        Метод для подготовки строки для логгирования.
        Используется декоратором log_it.

        Аргументы
        func - функция (объект)
        *args - кортеж неименованных аргументов
        **kwargs - словарь именованных аргументов
        """
        msg = ["called " + func.__name__ + "("]
        for i, v in enumerate(args):
            _str = str(v)
            if i != len(args) - 1:
                _str += ", "
            msg.append(_str)
        if len(args) > 0:
            msg.append(", ")
        for i, (k, v) in zip(range(len(kwargs)), kwargs.items()):
            _str = str(k) + ": " + str(v)
            if i != len(kwargs.items()) - 1:
                _str += ", "
            msg.append(_str)
        msg.append(")")
        return "".join(msg)


log = Logger()


def log_it(func: Any) -> Any:
    """
    Декоратор для встраивания логгирования вызовов функций (и их аргументов).

    Аргументы
    func - функция (объект)

    Пример использования:
    @log_it
    def test(*args, **kwargs):
        pass
    """
    @wraps(func)
    def wrapper(*args: Tuple, **kwargs: Dict) -> Any:
        log.info(Logger.form_string_from_args(func, *args, **kwargs))
        return func(*args, **kwargs)
    return wrapper


if __name__ == "__main__":

    @log_it
    def test(*args, **kwargs):
        return

    test(5, 7, level=logging.CRITICAL, file="file.txt")
    test()
