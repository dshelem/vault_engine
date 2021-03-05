"""
Модуль для инициализации структуры база данных.
Структура БД упрощенная, но удовлетворяющая требованиям ТЗ.

!!! Не запускайте модуль если вы абсолютно не уверены в том что делаете.
Все имеющиеся данные будут стерты!!!

Автор Денис Шелемех, 2021
"""

import sqlite3

from engine.config import config


db_file_name = config["STORAGE"]["DB_FILE_NAME"]
conn = sqlite3.connect(db_file_name)

cursor = conn.cursor()

setup_sql = """
DROP TABLE IF EXISTS tblVaults;

CREATE TABLE tblVaults
(
 Vault_ID          integer PRIMARY KEY NOT NULL,
 Vault_Name        text NOT NULL,
 Company_ID        integer NULL,
 UNIQUE (Company_ID, Vault_Name)
);

CREATE INDEX index_vault_name
ON tblVaults(Vault_Name);

CREATE INDEX index_company_id
ON tblVaults(Company_ID);

DROP TABLE IF EXISTS tblSecrets;

CREATE TABLE tblSecrets
(
 Secret_ID          integer PRIMARY KEY NOT NULL,
 Secret_Name        text NOT NULL,
 Secret_Description text NULL,
 Secret_Data        blob NOT NULL,
 Vault_ID           integer NOT NULL,
 UNIQUE (Vault_ID, Secret_Name),
 FOREIGN KEY (Vault_ID) REFERENCES tblVaults (Vault_ID) ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE INDEX index_secret_name
ON tblSecrets(Secret_Name);

CREATE INDEX index_vault_id
ON tblSecrets(Vault_ID);

CREATE INDEX index_secret_description
ON tblSecrets(Secret_Description);
"""

cursor.executescript(setup_sql)
conn.commit()

conn.close()
