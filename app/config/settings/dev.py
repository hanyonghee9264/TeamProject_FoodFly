from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

secrets = json.load(open(os.path.join(SECRETS_DIR, 'dev.json')))

ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = secrets['DATABASES']
