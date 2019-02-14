import os

from .base import *

INSTALLED_APPS.insert(0, 'django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

TEST_OUTPUT_DIR = os.environ.get('TEST_OUTPUT_DIR', '.')

NOSE_ARGS = [
    '--verbosity=2',
    '--nologcapture',
    '--with-spec',
    '--spec-color',
    '--with-xunit',
    f'--xunit-file={TEST_OUTPUT_DIR}/unittests.xml',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', None),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432')
    }
}
