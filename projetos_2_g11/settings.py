from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

TARGET_ENV = os.getenv('TARGET_ENV', 'dev')

# Ativa modo debug se não for produção
DEBUG = True

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-g1qu$9_0vz4^!9gdp00eqdztm1p#rf!gpikrc0diz)22pf3!ub'
)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'projetos-2-g11.onrender.com',
]

# Configuração inteligente do Banco de Dados
if TARGET_ENV == 'prod':
    # Se estiver na Azure, usa o caminho do servidor Linux
    DB_NAME = '/home/site/db.sqlite3'
else:
    # Se estiver no seu Windows, usa a pasta do projeto
    DB_NAME = BASE_DIR / 'db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_NAME,
    }
}

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'noticias',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projetos_2_g11.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'projetos_2_g11.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WHITENOISE_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CSRF_TRUSTED_ORIGINS = [
    "https://projetos-2-g11.onrender.com",
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
