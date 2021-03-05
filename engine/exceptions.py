"""
Модуль обработки неотловленных исключений
Автор Денис Шелемех, 2021
"""

import sys
from typing import Any
from traceback import format_exception

from engine import logger


def placeholder(exc_type: Any, value: Exception, traceback: Any) -> None:
    """
    Обработчик неотловленных исключений. Используется для назначения переменной
    sys.excepthook. Питон требует в обработчике использовать данную
    сигнатуру. Аргументы передаем в системную функцию format_exception для
    формирования строки для логгирования.

    Аргументы
    exc_type: тип исключения
    value: исключение
    traceback: трейсбэк
    """
    msg = ["*** EXCEPTION ***\n",
           *format_exception(exc_type, value, traceback)]
    logger.log.critical("".join(msg))


"""
Переопределяем хук на отлов необработанных исключений. Хук по умолчанию
продолжает храниться в sys.__excepthook__, - если его надо восстановить.
"""
sys.excepthook = placeholder


class StorageException(Exception):
    pass
