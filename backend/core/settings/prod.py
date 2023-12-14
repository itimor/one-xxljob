# -*- coding: utf-8 -*-
# author: itimor

import os

APP_ENV = 'prod'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '64318ob@vbou7h50)b0a_pfda4d$bw2nhl4h*m$qo0_e_fxw=658!z*x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'one',
        'USER': 'root',
        'PASSWORD': 'TY%pwd123',
        'HOST': 'localhost',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks=0;",
        }
    }
}

# 加载 jobapi
from utils.xxljob_api import XXLJOB

xxljob_info = {
    "api_url": "http://localhost:9090/xxl-job-admin",
    "username": "boce",
    "password": "Ql7SWRieWJ",
}
jobapi = XXLJOB(xxljob_info)

xxljob_db_info = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "passwd": "TY%pwd123",
        "db": "xxl_job",
}
