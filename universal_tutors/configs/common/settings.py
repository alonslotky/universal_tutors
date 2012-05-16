import os, django, urllib

# Base paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_SIMULATE_IP = '81.139.75.19'

ADMINS = ('ben@rawjam.co.uk',)
MANAGERS = ('Benjamin Dell', 'ben@rawjam.co.uk'),
ACCOUNT_ACTIVATION_ADMINS = ['ben@rawjam.co.uk',]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'universal_tutors',
        'USER': 'localuser',
        'PASSWORD': 'localuser',
        'HOST': 'localhost',
    }
}

# Local time
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-GB'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Media
STATIC_ROOT = os.path.join(SITE_ROOT, 'apps/common/static')
STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = "/static/grappelli/"

MEDIA_ROOT = os.path.join(SITE_ROOT, "media")
MEDIA_URL = "/media/"

SECRET_KEY = '%e!odn8_$$x_p2hw#su=h!@k!y57kljl)2h%(qn^t#72rqm8&-e'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "apps.common.utils.context_processors.app_wide_vars",
    "allauth.context_processors.allauth",
    "allauth.account.context_processors.account",
    #'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
    #'admintools_bootstrap.context_processors.site',
)

MIDDLEWARE_CLASSES = (
    #'apps.common.utils.middleware.AJAXSimpleExceptionResponse',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#    'johnny.middleware.LocalStoreClearMiddleware',
#    'johnny.middleware.QueryCacheMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'cms.middleware.page.CurrentPageMiddleware',
    #'cms.middleware.user.CurrentUserMiddleware',
)

if DEBUG:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.debug',)
if USE_I18N:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

ROOT_URLCONF = 'universal_tutors.configs.common.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (
    # Base Django Apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'grappelli.dashboard',
    'grappelli',
    #'admintools_bootstrap',
    #'admin_tools',
    #'admin_tools.theming',
    #'admin_tools.menu',
    #'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.markup',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'flatblocks',
    
    # Utilities & Helper Apps
    'south',
    'tinymce',
    'filebrowser',
    'django_extensions',
    'uni_form',
    'django_static',
#    'johnny',
    'tagging',
    'smart_selects',
    'pagination',
#    'haystack',
    
    # Registration, Signin and Account Management
    'emailconfirmation',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.twitter',
    'allauth.openid',
    'allauth.facebook',
    
    # Internal Apps
    'apps.common',
    'apps.core',
    'apps.profile',
    'apps.classes',
    
    # CMS
#    'cms',
#    'mptt',
#    'menus',
#    'cms.plugins.text',
#    'cms.plugins.picture',
#    'cms.plugins.link',
#    'cms.plugins.file',
#    'cms.plugins.snippet',
#    'cms.plugins.googlemap',
#    'cms.plugins.inherit',
#    'cms_search',
#    'apps.cmsplugin_contact',
#    'sekizai'
)

# MISC PROJECT SETTINGS
PROJECT_NAME = "Universal Tutors"
PROJECT_SITE_DOMAIN = '127.0.0.1:8000'
PROJECT_INFO_EMAIL_ADDRESS = 'universal_tutors@rawjam.co.uk'
CONTACT_EMAIL = "universal_tutors@rawjam.co.uk"
GOOGLE_ANALYTICS_CODE = "UA-XXXXX-X"
SHARETHIS_PUBLISHER_KEY = "f3129d97-8846-4ead-a850-726b9901d0f1"
GOOGLE_MAPS_API_KEY = ""
ADDTHIS_KEY = "ra-4d87f7de6c9ab011"
TWITTER_TIMEOUT = 300
EXEC_LOUNGE_BACKDOOR_KEY = "BN02ME1CNTMLEVG"
VER_NO = 0.9

DEFAULT_PROFILE_IMAGE = os.path.join(MEDIA_ROOT, 'uploads/universal_tutors/profile_portrait_default.png')

# DJANGO STATIC
DJANGO_STATIC = not DEBUG
DJANGO_STATIC_SAVE_PREFIX = os.path.join(MEDIA_ROOT, 'cache-forever')
DJANGO_STATIC_NAME_PREFIX = "cache-forever/"
if DEBUG:
    DJANGO_STATIC_MEDIA_URL = STATIC_URL
else:
    DJANGO_STATIC_MEDIA_URL = MEDIA_URL
DJANGO_STATIC_MEDIA_URL_ALWAYS = True
DJANGO_STATIC_MEDIA_ROOTS = [os.path.join(SITE_ROOT, 'apps/common/static'), STATIC_ROOT, MEDIA_ROOT]

# CACHE SETTINGS 
CACHE_BACKEND = 'johnny.backends.locmem://'
CACHE_MIDDLEWARE_KEY_PREFIX='universal_tutors:'
CACHE_MIDDLEWARE_SECONDS=90 * 60 # 90 minutes
CACHE_PREFIX = "universal_tutors:"
CACHE_COUNT_TIMEOUT = 60
JOHNNY_MIDDLEWARE_KEY_PREFIX='jc_universal_tutors'

# EMAIL SETTINGS
DEFAULT_FROM_EMAIL = 'noreply@rawjam.co.uk'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@rawjam.co.uk'
EMAIL_HOST_PASSWORD = '2M5394'

EMAIL_MANAGER = ['ben@rawjam.co.uk',]

# Authentication / Account Management Settings
AUTH_PROFILE_MODULE = 'profile.UserProfile'
LOGIN_URL = '/account/signin/'
LOGIN_REDIRECT_URL = "/dashboard/"
UNDER16_URL = '/account/under16/'
TYPE_URL = '/account/type/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_AVATAR_SUPPORT = False
EMAIL_CONFIRMATION_DAYS = 99
FACEBOOK_ENABLED = True
TWITTER_ENABLED = True
OPENID_ENABLED = True
SOCIALACCOUNT_ENABLED = True
DEFAULT_PROFILE_IMAGE = 'images/defaults/profile.png'

# DJANGO HAYSTACK SETTINGS
HAYSTACK_SITECONF = 'configs.common.search_sites'
HAYSTACK_SEARCH_ENGINE = "whoosh"
HAYSTACK_DEFAULT_OPERATOR = "OR"
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20
HAYSTACK_WHOOSH_PATH = os.path.join(SITE_ROOT, "whoosh_index")
HAYSTACK_WHOOSH_STORAGE = "file" # Can also be 'ram'
HAYSTACK_WHOOSH_POST_LIMIT = 256 * 1024 * 1024

# GRAPPELLI SETTINGS
GRAPPELLI_ADMIN_TITLE = 'Universal Tutors Administration'
GRAPPELLI_ADMIN_URL = '/admin'
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

# CMS settings
gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
)

CMS_TEMPLATES = (
#    ('cms/home.html', gettext('Home Page')),
#    ('cms/home2.html', gettext('Home Page 2')),
#    ('cms/global_offices.html', gettext('Global Offices')),
#    ('cms/media_centre.html', gettext('Media Centre')),
#    ('cms/subpage_simple.html', gettext('Standard Subpage')),
#    ('cms/subpage_simple_subbody.html', gettext('Standard Subpage - Sub Body')),
#    ('cms/subpage_simple_noblock.html', gettext('Standard Subpage - No Block')),
#    ('cms/subpage_simple_noblock_largelogo.html', gettext('Standard Subpage - No Block / Large Logo')),
#    ('cms/subpage_simple_notitle.html', gettext('Standard Subpage - No Title')),
#    ('cms/subpage_simple_nointro.html', gettext('Standard Subpage - No Intro')),
#    ('cms/full_width.html', gettext('Full Width (Black Background)')),
#    ('cms/full_width_whitebg.html', gettext('Full Width (White Background)')),
)

#CMS_PLACEHOLDER_CONF = {
#	'intro_paragraph': {
#    	"plugins": ('TextPlugin'),
#        "name":gettext("Intro Paragraph"),
#    },
#}

CMS_SOFTROOT = True
CMS_MODERATOR = False
CMS_PERMISSION = False
CMS_REDIRECTS = False
CMS_SEO_FIELDS = True
CMS_MENU_TITLE_OVERWRITE = True
CMS_SHOW_END_DATE = True
CMS_SHOW_START_DATE = True
CMS_URL_OVERWRITE = False
CMS_FLAT_URLS = False
CMS_CONTENT_CACHE_DURATION = 60
CMS_USE_TINYMCE = True
CMS_CACHE_PREFIX = "universal_tutors_branded:"
CMS_HIDE_UNTRANSLATED = False

CMS_PAGE_MEDIA_PATH = 'uploads/cms_media/'

# Django-filebrowser settings
FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL + "filebrowser/"
FILEBROWSER_PATH_FILEBROWSER_MEDIA = os.path.join(STATIC_URL, 'filebrowser/')
#FILEBROWSER_DIRECTORY = "uploads/"
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm','.swf'],
    'Document': ['.pdf','.doc','.rtf','.txt','.xls','.csv'],
    'Sound': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p'],
    'Code': ['.html','.py','.js','.css'],
    # for TinyMCE we also have to define lower-case items
    'image': ['Image'],
    'file': ['Folder','Image','Document',],
}

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'thumb': {'verbose_name': 'Grid Thumb', 'width': 150, 'height': 150, 'opts': 'crop upscale'},
    'small': {'verbose_name': 'Small (210px)', 'width': 210, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium (370px)', 'width': 370, 'height': '', 'opts': ''},
    'large': {'verbose_name': 'Large (530px)', 'width': 530, 'height': '', 'opts': ''},

    'class_list_profile_image': {'width': 61, 'height': 61, 'opts': 'crop upscale'},
    'profile_image': {'width': 175, 'height': 175, 'opts': 'crop upscale'},
    'list_tutors': {'width': 67, 'height': 67 , 'opts': 'crop upscale'},
    'homepage_list_tutors': {'width': 79, 'height': 79 , 'opts': 'crop upscale'},
}
FILEBROWSER_ADMIN_VERSIONS = [
    'thumb', 'small','medium','large',
]
FILEBROWSER_ADMIN_THUMBNAIL = 'fb_thumb'
FILEBROWSER_IMAGE_MAXBLOCK = 1024*1024
FILEBROWSER_MAX_UPLOAD_SIZE = 10485760 # 10485760 bytes = about 10megs

TINYMCE_JS_URL = ADMIN_MEDIA_PREFIX + "tinymce/jscripts/tiny_mce/tiny_mce.js"
TINYMCE_JS_ROOT = os.path.join(MEDIA_ROOT, 'grappelli/tinymce/jscripts/tiny_mce/')



#TINYMCE_JS_URL = MEDIA_URL + 'admin/tinymce/jscripts/tiny_mce/tiny_mce.js'
# file system path to the files
#TINYMCE_JS_ROOT = os.path.join(MEDIA_ROOT, "admin","tinymce", "jscripts", "tiny_mce")
#TINYMCE_FILEBROWSER = True # if you have installed  django-filebrower
#TINYMCE_DEFAULT_CONFIG = {
#    'relative_urls'     : False,
#    'height'            : 400,
#    'width'             : 640,
#    'mode'              : "textareas",
#    'theme'             : "advanced",
#    'language'          : "en",
#    'skin'              : "grappelli",
#    'browsers'          : "gecko, safari"
#}

# SCRIBBLAR_API_KEY
SCRIBBLAR_API_KEY = "4E05E226-B564-8140-D1E65546167F353C"

#CONTACT
CONTACT_EMAIL = ['nick@universaltutors.com']

# Allow for local (per-user) override
try:
    from local_settings import *
except ImportError:
    pass


