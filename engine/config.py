"""
Модуль определения считывателя системной конфигурации
Автор Денис Шелемех, 2021
"""

import configparser
import sys

config_file_name = "config.ini"

config = configparser.ConfigParser()

try:
    config.read(config_file_name)
except FileNotFoundError:
    sys.stderr.write("Cannot open configuration file " + config_file_name)
    sys.exit(1)

config['ENCRYPTION']['OPEN_SSL_PATH'] = \
    config['ENCRYPTION']['OPEN_SSL_PATH_WIN32']

for os in ["linux", "darwin"]:
    if os in sys.platform:
        config['ENCRYPTION']['OPEN_SSL_PATH'] = \
            config['ENCRYPTION']['OPEN_SSL_PATH_LINUX']
