from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

secrets = json.load(open(os.path.join(SECRETS_DIR, 'dev.json')))

ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']

# Application definition
INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = secrets['DATABASES']

# S3 Media config
# DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
# AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']

# django toolbar
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = [
    '127.0.0.1',
]
