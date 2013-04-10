from universal_tutors.configs.common.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'universal_tutors',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    }
}

ACCOUNT_ACTIVATION_ADMINS = ['ben@rawjam.co.uk',]

# Project settings and active names
PROJECT_SITE_DOMAIN = 'universaltutors.rawjam.co.uk'
PROJECT_INFO_EMAIL_ADDRESS = 'info@universaltutors.com'

# Caching
CACHE_BACKEND = 'johnny.backends.memcached://127.0.0.1:11211'

# If you want to use Django Debug Toolbar, you need to list your IP address here
INTERNAL_IPS = ('0.0.0.0')

# Email addresses
MANAGERS = (
    ('Benjamin Dell', 'ben@rawjam.co.uk'),
)

# GOOGLE
GOOGLE_ANALYTICS_CODE = None


# Paypal
PAYPAL_SENDER_EMAIL = "nick@universaltutors.com"
PAYPAL_RECEIVER_EMAIL = "nick@universaltutors.com"
PAYPAL_API_APPLICATION_ID = "APP-9G278759L8342450A"
PAYPAL_API_USERNAME = "nick_api1.universaltutors.com"
PAYPAL_API_PASSWORD = "N86TYAFKUS34AU4B"
PAYPAL_API_SIGNATURE = "AFcWxV21C7fd0v3bYYYRCpSSRl31A7bLYNJ-VWMgxPgU.mcP.bGCu5cR"
PAYPAL_TEST = True
PAYPAL_IMAGE = 'https://www.sandbox.paypal.com/en_US/i/btn/btn_buynowCC_LG.gif'



# logging
import logging.config
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(LOG_FILENAME)

DJANGO_STATIC = True
DJANGO_STATIC_SAVE_PREFIX = os.path.join(MEDIA_ROOT, 'cache-forever')
DJANGO_STATIC_NAME_PREFIX = "cache-forever/"
DJANGO_STATIC_MEDIA_URL = MEDIA_URL
DJANGO_STATIC_MEDIA_URL_ALWAYS = True
DJANGO_STATIC_MEDIA_ROOTS = [os.path.join(SITE_ROOT, 'apps/common/static'), STATIC_ROOT, MEDIA_ROOT]
