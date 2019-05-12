'''
开发环境设置
'''

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'HOST': os.getenv("DB_HOST"),
        # 'PORT': os.getenv("DB_PORT"),
        'USER': "root",
        'PASSWORD': "root",
        'NAME': "oj",
    }
}