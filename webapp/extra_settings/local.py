# -*- coding: utf-8 -*-

import os.path as op

PROJECT_ROOT = op.dirname(op.dirname(op.abspath(__file__)))
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",        # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "test",                       # Or path to database file if using sqlite3.
        "USER": "tester",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "localhost",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "ROOT_TAG_EXTRA_ATTRS": "ng-non-bindable"  # angular ile çakışmaması için
}

EMAIL_DEBUG = DEBUG
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_SENDER = "tester@example.com"
EMAIL_FILE_PATH = 'mails_log'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    "django_extensions",
    "debug_toolbar",
    "main",
]

INTERNAL_IPS = ('127.0.0.1',)
