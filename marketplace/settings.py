# marketplace/settings.py
from pathlib import Path
from decouple import config
import os

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['*']  # We'll configure this properly later

# For Windows development
import sys
if sys.platform == 'win32':
    import platform
    if platform.release() == '11':  # Windows 11
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')

# marketplace/settings.py

# Application definition
SHARED_APPS = [
    'django_tenants',  # Must be first
    'apps.customers',  # Contains Tenant and Domain models
    
    # Django apps that should be in public schema
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

TENANT_APPS = [
    # Django apps that should be in tenant schemas
    'django.contrib.admin',
    
    # Your tenant-specific apps
    'apps.products',
    'apps.orders',
    'apps.cart',
]

INSTALLED_APPS = SHARED_APPS + TENANT_APPS


# marketplace/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',  # Special backend
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'options': '-c search_path=public'  # Default to public schema
        }
    }
}

# Django-tenants specific settings
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)



MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # Must be first
    'apps.customers.middleware.TenantDebugMiddleware',       # Our debug middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Enable logging to see middleware output
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
# marketplace/settings.py

# Tenant settings
TENANT_MODEL = "customers.Tenant"  # The model that stores tenant information
TENANT_DOMAIN_MODEL = "customers.Domain"  # The model that maps domains to tenants

# Public schema URL configuration
PUBLIC_SCHEMA_URLCONF = 'marketplace.urls_public'

# Windows-specific settings for development
if DEBUG and sys.platform == 'win32':
    # This helps with Windows path issues
    FORCE_SCRIPT_NAME = ''

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # You can use [] if you have no custom templates yet
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

 # ← MUST be the public one!

PUBLIC_SCHEMA_URLCONF = 'marketplace.urls_public'
TENANT_URLCONF = 'marketplace.urls_tenant'


# marketplace/settings.py

# Add these tenant-specific settings
PUBLIC_SCHEMA_NAME = 'public'
PUBLIC_SCHEMA_URLCONF = 'marketplace.urls_public'  # URLs for public schema
ROOT_URLCONF = 'marketplace.urls'  # URLs for tenant schemas

# This tells django-tenants which schema is public
TENANT_TYPES = {
    'public': {
        'APPS': SHARED_APPS,
        'URLCONF': 'marketplace.urls_public',
    },
    'default': {
        'APPS': TENANT_APPS,
        'URLCONF': 'marketplace.urls',
    }
}

# marketplace/settings.py

import os

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files configuration  
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Tenant-specific media files
# Each tenant can have separate media folders
MULTITENANT_RELATIVE_MEDIA_ROOT = "tenant/%s"  # %s will be replaced with schema_name

# marketplace/settings.py (add Docker support)
# marketplace/settings.py (add at the top after imports)
import os

# Check if running in Docker
IS_DOCKER = os.environ.get('IS_DOCKER', False)

# Update ALLOWED_HOSTS
ALLOWED_HOSTS = ['*'] if IS_DOCKER else ['localhost', '127.0.0.1', '.localhost']

# Update database configuration
if IS_DOCKER:
    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': os.environ.get('DB_NAME', 'marketplace_db'),
            'USER': os.environ.get('DB_USER', 'marketplace_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'marketplace123'),
            'HOST': os.environ.get('DB_HOST', 'db'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }