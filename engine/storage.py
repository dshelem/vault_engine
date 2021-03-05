"""
Модуль определения класса хранилища
Автор Денис Шелемех, 2021
"""

import sqlite3
from typing import List

from engine.config import config
from engine.logger import log_it
from engine.connection import DBConnection
from engine.exceptions import StorageException


class Storage:
    """
    Класс хранилища.Синглтон
    """
    # кол-во экземпляров класса
    instances = 0

    @classmethod
    @log_it
    def init(cls) -> None:
        """
        Метод гарантирует конструирование класса в качестве синглтона
        Используется методом __init__()

        Аргументы
        cls - класс(объект)
        """
        if cls.instances > 0:
            raise RuntimeError(cls.__name__ + " is a singleton class")
        else:
            cls.instances += 1

    @log_it
    def __init__(self) -> None:
        Storage.init()
        self.db_file_name = config["STORAGE"]["DB_FILE_NAME"]

    @log_it
    def get_vault_id(self, vault_name: str) -> int:
        """
        Возвращает ID сейфа с именем vault_name
        При его отсутствии создает сейф с таким именем и возвращает ID

        Аргументы
        vault_name - строка - имя сейфа
        """
        with DBConnection(self.db_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute("select Vault_ID from tblVaults "
                           "where Vault_Name = ?;", (vault_name, ))
            result = cursor.fetchone()
            if not result:
                cursor.execute("insert into tblVaults (Vault_Name) "
                               "values (?);", (vault_name, ))
                return cursor.lastrowid
            else:
                return result[0]

    @log_it
    def get_secret_id_from_secret_name(self, secret_name: str) -> int:
        """
        Возвращает ID секрета с именем secret_name
        При его отсутствии в БД кидает исключение StorageException

        Аргументы
        secret_name - строка - имя секрета
        """
        with DBConnection(self.db_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute("select Secret_ID from tblSecrets where "
                           "Secret_Name = ?;", (secret_name, ))
            result = cursor.fetchone()
            if not result:
                raise DBConnection("There is no secret with name "
                                   + str(secret_name))

            return result[0]

    @log_it
    def insert_secret(self, vault_name: str, secret_name: str,
                      secret_data: str, secret_description: str = "") -> int:
        """
        Размещает секрет в сейфе. Возвращает ID вставленной записи.
        Кидает исключение StorageException если такой секрет существует

        Аргументы
        vault_name - строка - имя сейфа
        secret_name - строка - имя секрета
        secret_data - строка - данные секрета
        secret_description - строка - описание секрета
        """
        vault_id = self.get_vault_id(vault_name=vault_name)
        with DBConnection(self.db_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute("select Secret_ID from tblSecrets where "
                           "Vault_ID = ? and Secret_Name = ?;",
                           (vault_id, secret_name, ))
            result = cursor.fetchone()
            if result:
                raise StorageException("Storage already has secret with name "
                                       + str(secret_name))
            else:
                cursor.execute("insert into tblSecrets "
                               "(Secret_Name, Secret_Data, "
                               "Secret_Description, Vault_ID) "
                               "values (?, ?, ?, ?);",
                               (secret_name, secret_data, secret_description,
                                vault_id, ))
            return cursor.lastrowid

    @log_it
    def get_secrets_list(self, **kwargs) -> List:
        """
        Возвращает список секретов из сейфа

        Аргументы
        vault_name - строка - имя сейфа
        ИЛИ
        vault_id - целое - ID сейфа
        """
        with DBConnection(self.db_file_name) as conn:
            cursor = conn.cursor()
            if kwargs.get("vault_id", None) is None:
                if kwargs.get("vault_name", None) is None:
                    raise ValueError("Ommited one of the mandatory "
                                     "parameters: vault_id, vault_name")
                else:
                    vault_id = self.get_vault_id(kwargs["vault_name"])
            else:
                vault_id = kwargs["vault_id"]

            cursor.execute("select Secret_ID, Secret_Name, Secret_Description "
                           "from tblSecrets where Vault_ID = ?;", (vault_id, ))
            return cursor.fetchall()

    @log_it
    def get_secret(self, secret_id: int) -> sqlite3.Row:
        """
        Возвращает строку - секрет

        Аргументы
        secret_id - целое - ID сейфа
        """
        with DBConnection(self.db_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute("select Secret_ID, Secret_Name, "
                           "Secret_Description, Secret_Data, Vault_ID "
                           "from tblSecrets where Secret_ID = ?;",
                           (secret_id, ))
            return cursor.fetchone()


storage = Storage()

if __name__ == '__main__':
    vault_id = storage.get_vault_id("Vault1")
    print("vault_id = ", vault_id)
    # storage.insert_secret(vault_name="Vault1", secret_name="Secret2",
    # secret_data="blah blah")
    # secret_id = storage.insert_secret(vault_name="Vault1",
    # secret_name="Secret3", secret_data="blah blah")
    rows = storage.get_secrets_list(vault_name="Vault1")
    print("rows = ", rows)
    print("secret = ", storage.get_secret(secret_id=3))
