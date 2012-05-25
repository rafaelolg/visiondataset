"""
These settings overrides what's in settings/base.py
"""

import logging

# To extend any settings from settings/base.py here's an example:
#from . import base
#INSTALLED_APPS = base.INSTALLED_APPS + ['debug_toolbar']

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '%(project_name)s',
            'USER': '%(user)s',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            }
        }
# Uncomment this and set to all slave DBs in use on the site.
# SLAVE_DATABASES = ['slave']
# Recipients of traceback emails and other notifications.

ADMINS = (
     ('Rafael Lopes', 'rafael'),
)
MANAGERS = ADMINS
TIME_ZONE = 'America/Sao_Paulo'

CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            }
        }

DEBUG = %(debug)s
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
DEV = %(debug)s
SECRET_KEY = '9sbj=it#)$exj3w5!hqtq*^$^se-(1=ywov-b*v_r3!eoufa=h'

LOG_LEVEL = logging.INFO
HAS_SYSLOG = True
SYSLOG_TAG = "http_app_visiondataset"  # Make this unique to your project.
# Remove this configuration variable to use your custom logging configuration
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'loggers': {
        'visiondataset': {
            'level': "DEBUG"
        }
    }
}

# Common Event Format logging parameters
#CEF_PRODUCT = 'visiondataset'
#CEF_VENDOR = 'Your Company'
#CEF_VERSION = '0'
#CEF_DEVICE_VERSION = '0'

INTERNAL_IPS = ('127.0.0.1')

# Enable these options for memcached
#CACHE_BACKEND= "memcached://127.0.0.1:11211/"
#CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True

# Set this to true if you use a proxy that sets X-Forwarded-Host
#USE_X_FORWARDED_HOST = False
SERVER_EMAIL = "rafaellg@vision.ime.usp.br"
DEFAULT_FROM_EMAIL = "rafaellg@vision.ime.usp.br"
SYSTEM_EMAIL_PREFIX = "[visiondataset]"
