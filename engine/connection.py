"""
Модуль определения класса соединения с БД (context manager)
Автор Денис Шелемех, 2021
"""

import sqlite3
from typing import Any

from engine.logger import log_it


class DBConnection:
    """
    Класс соединения с БД
    """
    @log_it
    def __init__(self, db_file_name: str) -> None:
        self.connection = sqlite3.connect(db_file_name)

    @log_it
    def __enter__(self) -> sqlite3.Connection:
        """
        "Магический" метод для открытия и возврата соединения с использованием оператора with
        Пример:
        with DB_Connection("db_name.db"):
            ...
        :return: объект sqlite3.Connection
        """
        return self.connection

    @log_it
    def __exit__(self, exc_ty: Any, exc_val: Exception, exc_tb: Any) -> None:
        """
        "Магический" метод для коммита и закрытия соединения при выходе из блока видимости оператора with
        """
        self.connection.commit()
        self.connection.close()
