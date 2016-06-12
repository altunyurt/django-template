# -*- coding: utf-8 -*-

import os
import os.path as op

PROJECT_ROOT = op.dirname(op.dirname(op.abspath(__file__)))
print PROJECT_ROOT
PROJECT_REAL_NAME = os.path.basename(PROJECT_ROOT)
PROJECT_NAME = "webapp"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            '%s/templates/' % PROJECT_ROOT,
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'environment': 'utils.template.jinja2_environment'
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]



# APP settings
VERIFICATION_REQUIRED = True
