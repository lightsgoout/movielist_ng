"""
Django settings for movielist_ng project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_7+4vyup^8+)@=czqy!g_zdnf41gycu$-(fce4fleamoc!6ya_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    'www.mvlst.com',
    'mvlst.com',
]


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'shell_plus',
    'social_auth',
    'registration',
    'ajax_select',
    'django_extensions',
    'djangobower',
    'django_activeurl',
    'statici18n',

    'achievements',
    'accounts',
    'common',
    'imports',
    'movies',
    'timeline',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'common.middleware.request_lang.RequestLangMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    'static',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

# noinspection PyUnresolvedReferences
STATIC_ROOT = 'compiledstatic'
STATICI18N_ROOT = 'static'
STATICI18N_PACKAGES = (
    ('app',)
)

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'static')

BOWER_INSTALLED_APPS = (
    'angular#1.3.14',
    'angular-animate#1.3.14',
    'angular-ui-utils#0.2.2',
    'angular-resource#1.3.14',
    'angular-route#1.3.14',
    'ngInfiniteScroll#1.2.0',
    'ng-tags-input#2.2.0',
    'bootstrap#3.3.2',
    'bootstrap-social#4.8.0',
    'jquery#2.1.3',
    'font-awesome#4.2.0',
    'angular-xeditable#0.1.8',
    'flag-icon-css#0.7.0',
    'bootstrap-hover-dropdown#2.1.3',
    'd3#3.5.5',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

AUTH_USER_MODEL = 'accounts.MovielistUser'

OMDB_LOGIN = 'enderstd@gmail.com'

ACCOUNT_ACTIVATION_DAYS = 7

AJAX_LOOKUP_CHANNELS = {
    'movie': ('movies.lookups', 'MovieLookup'),
    'person': ('movies.lookups', 'PersonLookup'),
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.EmailBackend',
)

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['json']

SEARCH_RESULTS_PER_PAGE = 100
SEARCH_QUERY_MINIMUM_LENGTH = 3

X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
