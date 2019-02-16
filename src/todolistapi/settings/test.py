import os

from .base import *

INSTALLED_APPS += ('django_nose', )

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DEBUG = True

ALLOWED_HOSTS = ['*']

NOSE_ARGS = [
    '--verbosity=2',
    '--nologcapture',
    '--with-spec',
    '--spec-color',
    '--with-xunit',
    f'--xunit-file=unittests.xml',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', None),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432')
    }
}
