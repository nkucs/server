'''
生产环境设置
'''

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = "path/to/data"

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'HOST': os.getenv("DB_HOST"),
        # 'PORT': os.getenv("DB_PORT"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_USER_PASSWORD"),
        'NAME': os.getenv("DB_NAME"),
    }
}