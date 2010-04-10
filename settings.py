# -*- coding: utf8 -*-

import os.path

def SELF_DIR(filename=''):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)

# Django settings for knowledge project.
# fuck lighttpd
FORCE_SCRIPT_NAME = ''

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('vladimir', 'vladimirbright@gmail.com'),
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE   = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME     = 'knowledgedb'             # Or path to database file if using sqlite3.
DATABASE_USER     = 'knowledge'             # Not used with sqlite3.
DATABASE_PASSWORD = 'supersuperkn'         # Not used with sqlite3.
DATABASE_HOST     = '127.0.0.1'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT     = ''             # Set to empty string for default. Not used with sqlite3.

# Настройки сфинкс 
SPHINX_SERVER = '127.0.0.1'
SPHINX_PORT = 9312
# Настройки кеша.
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = SELF_DIR('s')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/s/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

LOGIN_URL='/login/'
# Настройки для по страничного вывода
PER_PAGE=15
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
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'knowledge.urls'

TEMPLATE_DIRS = (
    SELF_DIR('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'knowledge.users',
    'knowledge.cards',
    'knowledge.feeds',
)
