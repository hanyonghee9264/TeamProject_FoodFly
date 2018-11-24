from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

secrets = json.load(open(os.path.join(SECRETS_DIR, 'production.json')))

ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = secrets['DATABASES']

# S3 Media config
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'ap-northeast-2'
