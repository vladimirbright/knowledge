# -*- coding: utf-8 -*-

import os.path

def self_dir(filename=''):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)

# fuck lighttpd
FORCE_SCRIPT_NAME = ''

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ( '127.0.0.1', '127.0.1.1' )
ALLOWED_HOSTS = ("*",)

ADMINS = (
     ( 'vladimir', 'vladimirbright@gmail.com' ),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': self_dir('db.sqlite3'),
    }
}

# PostgreSQL configuration (commented out for development)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'knowledgedb',
#         'USER': 'knowledge',
#         'PASSWORD': 'supersuperkn',
#         'HOST': '127.0.0.1',
#         'PORT': '',
#     }
# }

# Настройки email
DEFAULT_FROM_EMAIL = 'site@knbase.org'
EMAIL_SUBJECT_PREFIX = '[knbase.org]'

TIME_ZONE = 'UTC'

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

# Modern Django templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [self_dir('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'cards.context_processors.get_favorites',
                'cards.context_processors.get_categories',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'pagination.middleware.PaginationMiddleware',  # Disabled
]

LOCALE_PATHS = (
    self_dir('locale'),
)

ROOT_URLCONF = 'urls'

# Template dirs now handled by TEMPLATES setting

# Context processors now handled by TEMPLATES setting

# Auto-generated primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = (
    'cards',
    # 'disqus',  # Temporarily disabled due to Django compatibility
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    # 'django.contrib.comments',  # Removed in Django 1.8+
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',  # Required for admin
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'feeds',
    # 'pagination',  # Temporarily disabled due to Python 2 syntax
    'sitemap',
    # 'south',  # Replaced by Django built-in migrations
    'users',
)

DISQUS_API_KEY = 'FOOBARFOOBARFOOBARFOOBARFOOBARF'
DISQUS_WEBSITE_SHORTNAME = 'knbase'


try:
    from local_settings import *
except ImportError:
    pass

