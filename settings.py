# -*- coding: utf8 -*-

import os.path

def SELF_DIR(filename=''):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)

# fuck lighttpd
FORCE_SCRIPT_NAME = ''

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ( '127.0.0.1', '127.0.1.1')

ADMINS = (
     ('vladimir', 'vladimirbright@gmail.com'),
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'knowledgedb',
        'USER': 'knowledge',
        'PASSWORD': 'supersuperkn',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# Настройки сфинкс 
SPHINX_SERVER = '127.0.0.1'
SPHINX_PORT = 9312
# Настройки кеша.
CACHE_BACKEND = 'johnny.backends.memcached://127.0.0.1:11211/'
JOHNNY_MIDDLEWARE_KEY_PREFIX='johnny'

# Настройки email
DEFAULT_FROM_EMAIL = 'site@knbase.org'
EMAIL_SUBJECT_PREFIX = '[knbase.org]'

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = SELF_DIR('s')

MEDIA_URL = '/s/'

ADMIN_MEDIA_PREFIX = '/media/'

LOGIN_URL='/login/'

# Настройки для по страничного вывода
PER_PAGE=5
PAGE_GET='page'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^l=_o)jzhczkcw=9#vpwiq22496^as$rip8&h*323)wn-p0-zs'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    SELF_DIR('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = [
        "django.core.context_processors.auth",
        "django.core.context_processors.i18n",
        "django.core.context_processors.request",
        "django.core.context_processors.media",
]

if DEBUG:
    TEMPLATE_CONTEXT_PROCESSORS.append("django.core.context_processors.debug")

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.sitemaps',
    'users',
    'sitemap',
    'cards',
    'feeds',
    'johnny',
    'south',
)

try:
    from local_settings import *
except ImportError:
    pass

