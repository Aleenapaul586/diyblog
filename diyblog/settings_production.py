from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your PythonAnywhere domain to allowed hosts
ALLOWED_HOSTS = ['aleen.pythonanywhere.com']  # Replace with your actual username

# Static files configuration
STATIC_ROOT = '/home/aleen/diyblog/static'  # Replace with your actual username
MEDIA_ROOT = '/home/aleen/diyblog/media'    # Replace with your actual username

# Configure database (use default SQLite configuration)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/aleen/diyblog/db.sqlite3',  # Replace with your actual username
    }
}

# Whitenoise configuration
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Optimize file handling
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB 