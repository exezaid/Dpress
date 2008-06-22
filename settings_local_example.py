# Django settings for paroblog project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alberto Paro', 'alberto@ingparo.it'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'djangopress'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Europe/Rome'

DIARIO_DEFAULT_MARKUP_LANG = 'rest'
DIARIO_DEFAULT_MARKUP_LANG = 10
 
BLOG_NAME = 'Blog Name'
TAGLINE = 'Everyone will like it'
DEFAULT_FROM_EMAIL = ''
SITE_URL = 'http://my.blog.us'

THEME = 'lite'

# Sample static pages links
STATIC_PAGES = (
#    ('About', '/about/', 'About me'),
#    ('Blog', '/blog/', 'Main place'),
#    ('Dev', 'http://byteflow.su/', 'Take a look at the code and development'),
#    ('', '', ''),
    )

# Set this to true to get first comment by any user autoapproved
ANONYMOUS_COMMENTS_APPROVED = False

# Possible choices are: ''|'simple'|'recaptcha'
# To utilize recaptcha you must get public/private keys
# from http://recaptcha.net/
CAPTCHA='simple'
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY =''

ENABLE_SAPE = False # Set this to true to enable Sape.ru client
ENABLE_IMPORT = False # Set this to true to enable WordPress importer
GA_ACC = '' # Google Analytics account
LI_ACC = False # Set True if you want liveinternet.ru counter
GMAPS_ACC = '' # Google Maps account
GRAVATAR_ENABLE = False # Enable gravatars?
SHORT_POSTS_IN_FEED = False # Full or short posts in feed
WYSIWYG_ENABLE = False # WYSIWYG for post text in admin
RENDER_METHOD = 'markdown' # Choices: bbcode and simple. Don't use html here, it is unsafe

# SOCIAL_BOOKMARKS can be reconfigured to contain values from apps/blog/templatetags/bookmarks.py
# BLOG_URLCONF_ROOT can be set if you want to remove 'blog/' prefix
# URL_PREFIX can be set to add url prefix to *all* urls

# Livejournal crossposting
ENABLE_LJ_CROSSPOST = False
LJ_USERNAME = ''
LJ_PASSWORD = ''

# DEBUG must be False in production mode
# Please read http://byteflow.su/wiki/DEBUG
DEBUG = True

# Set it to True if you want to activate orm_debug template tag
# You also need to setup INTERNAL_IPS setting 
# if you want to use explain feature of orm_debug
ORM_DEBUG = False
