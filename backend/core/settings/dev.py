# -*- coding: utf-8 -*-
# author: itimor

import os

APP_ENV = 'dev'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '64318ob@vbou7h50)b0a_pfda4d$bw2nhl4h*m$qo0_e_fxw=658!z*x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sqlite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, '../core.db'),
#     }
# }

# mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'one',
        'USER': 'root',
        'PASSWORD': 'momo520',
        'HOST': '1.1.1.11',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks=0;",
        }
    }
}

# 加载 mysql
import pymysql
pymysql.install_as_MySQLdb()


# 加载 jobapi
from utils.xxljob_api import XXLJOB

xxljob_info = {
    "api_url": "http://1.1.1.11:9090/xxl-job-admin",
    "username": "admin",
    "password": "123456",
}
jobapi = XXLJOB(xxljob_info)

xxljob_db_info = {
        "host": "1.1.1.11",
        "port": 3306,
        "user": "root",
        "passwd": "momo520",
        "db": "xxl_job",
}