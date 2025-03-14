
from pathlib import Path
from environ import Env

env = Env()
Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^=6-_k)oh!n9-fpcd1qd0rf(!8y2!!8cc*so1if(!*ydv@*_dc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    'https://sandbox.sslcommerz.com',
    'https://easygrocery-server.vercel.app',
    'https://easygrocery.vercel.app',
    'http://localhost:3000',
    'http://127.0.0.1:8000',
]

CORS_ALLOWED_ORIGINS = [
    'https://sandbox.sslcommerz.com',
    'https://easygrocery-server.vercel.app',
    'https://easygrocery.vercel.app',
    'http://localhost:3000',
    'http://127.0.0.1:8000'
]

# Application definition

INSTALLED_APPS = [
    # vercel requirement
    "whitenoise.runserver_nostatic",

    # cloud image
    "cloudinary",
    "cloudinary_storage",

    # system app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',

    # drf
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',

    # project app
    'user',
    'category',
    'product',
    'order',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mysite.wsgi.app'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  
        'NAME': 'neondb',                         
        'USER': 'neondb_owner',                   
        'PASSWORD': 'npg_i5JZSTWt6OAa',   
        'HOST': 'ep-misty-pine-a1vrheva-pooler.ap-southeast-1.aws.neon.tech', 
        'PORT': 5432,                          
        'OPTIONS': {
            'sslmode': 'require', 
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Email Send
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env('HOST_EMAIL')
EMAIL_HOST_PASSWORD = env('HOST_EMAIL_PASSWORD')


# Payment Gateway
SSLCOMMERZ = {
    "STORE_ID": "testbox",
    "STORE_PASSWORD": "qwerty",
    "ISSANDBOX": True,
    "CURRENCY": "BDT",
}

# Cloudinary Storage
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": env('CLOUDINARY_CLOUD_NAME'),
    "API_KEY": env('CLOUDINARY_API_KEY'),
    "API_SECRET": env('CLOUDINARY_API_SECRET')
}

# Use Cloudinary for media file storage
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
