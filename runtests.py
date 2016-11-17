#!/usr/bin/env python
import django
django.setup()
import sys
import os
from os.path import dirname, abspath
from optparse import OptionParser

from django.conf import settings

# For convenience configure settings if they are not pre-configured or if we
# haven't been provided settings to use by environment variable.
if not settings.configured and not os.environ.get('DJANGO_SETTINGS_MODULE'):
    settings.configure(
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))),

        SECRET_KEY = '0c2_x_ixxb1wg%7y2_-=mx-03(h)=327_9uc8b-gvuew2*#o!%',

        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        AUTHENTICATION_BACKENDS = ("secure_login.backends.SecureLoginBackend", ),
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'secure_login',
        ],
        STATIC_URL = "/static/",
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                # 'DIRS': [
                #     os.path.join(BASE_DIR,"templates"),
                # ],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ],
        LANGUAGE_CODE = 'en-us',

        TIME_ZONE = 'UTC',

        USE_I18N = True,

        USE_L10N = True,

        USE_TZ = False,
    )

# from django.test.simple import DjangoTestSuiteRunner
from django.test.runner import DiscoverRunner

def runtests(*test_args, **kwargs):
    if not test_args:
        test_args = ['secure_login']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    test_runner = DiscoverRunner(
        verbosity=kwargs.get('verbosity', 1),
        interactive=kwargs.get('interactive', False),
        failfast=kwargs.get('failfast'))
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--failfast', action='store_true', default=False, dest='failfast')
    (options, args) = parser.parse_args()
    runtests(failfast=options.failfast, *args)
