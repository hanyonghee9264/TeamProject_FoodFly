from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

secrets = json.load(open(os.path.join(SECRETS_DIR, 'production.json')))

ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = secrets['DATABASES']

