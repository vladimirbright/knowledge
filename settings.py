# -*- coding: utf-8 -*-

import os.path

def self_dir(filename=''):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)

# fuck lighttpd
FORCE_SCRIPT_NAME = ''

DEBUG = False
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ( '127.0.0.1', '127.0.1.1' )

ADMINS = (
     ( 'vladimir', 'vladimirbright@gmail.com' ),
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

# Настройки email
DEFAULT_FROM_EMAIL = 'site@knbase.org'
EMAIL_SUBJECT_PREFIX = '[knbase.org]'

TIME_ZONE = None

LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

USE_I18N = True

STATICFILES_DIRS = (
    self_dir('assets'),
)
STATIC_ROOT = self_dir('s')
STATIC_URL = '/s/'
MEDIA_ROOT = self_dir('media')
MEDIA_URL = '/media/'


ADMIN_MEDIA_PREFIX = '/media/'
LOGIN_URL='/login/'

# Настройки для по страничного вывода
PER_PAGE=5
PAGE_GET='page'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^l=_o)jzhczkcw=9#vpwiq22496^as$rip8&h*323)wn-p0-zs'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'pagination.middleware.PaginationMiddleware',
)

LOCALE_PATHS = (
    self_dir('locale'),
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    self_dir('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.request",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",

        "cards.context_processors.get_favorites",
        "cards.context_processors.get_categories",
)


INSTALLED_APPS = (
    'cards',
    'disqus',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'feeds',
    'pagination',
    'sitemap',
    'south',
    'users',
)

DISQUS_API_KEY = 'FOOBARFOOBARFOOBARFOOBARFOOBARF'
DISQUS_WEBSITE_SHORTNAME = 'knbase'


try:
    from local_settings import *
except ImportError:
    pass

