DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

SITE_ID = 303
DEBUG = True
TEMPLATE_DEBUG = DEBUG
TESTING = DEBUG
SECRET_KEY = "abc"

DATABASES = {"default": {
    "NAME": ":memory:",
    "ENGINE": "django.db.backends.sqlite3",
    "USER": '',
    "PASSWORD": '',
    "PORT": '',
}}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'object_log',
)

ROOT_URLCONF = 'test_urls'

TEMPLATE_DIRS = ('test_templates', )
