import os.path
import sys


# Getting Started
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'applications'))

# Debug Settings
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Basic Settings
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'

# Site Settings
SITE_ID = 1
ROOT_URLCONF = 'urls'
USE_I18N = True

# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'core.middleware.url.UrlMiddleware', # Custom Middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)
USE_ETAGS = True
APPEND_SLASH = True
REMOVE_WWW = True

# Template Settings
MARKUP_FILTER = ('markdown', {})
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
GENERIC_CONTENT_LOOKUP_KWARGS = {
    'blog.entry': { 'status': 1 }
}

# Secret Key Generator
if not hasattr(globals(), 'SECRET_KEY'):
    SECRET_FILE = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            SECRET_KEY = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            raise Exception('Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)
        
    

# Tagging (django-tagging)
FORCE_LOWERCASE_TAGS = True

# Import Local Settings
try:
    from locals import *
except ImportError:
    pass

# Cache Settings
if DEBUG:
    CACHE_BACKEND = "dummy:///"
else:
    CACHE_BACKEND = "memcached://172.18.0.39:11211/"
    CACHE_MIDDLEWARE_SECONDS = 60 * 60
    CACHE_MIDDLEWARE_KEY_PREFIX = 'plugables'
