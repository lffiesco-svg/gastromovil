from datetime import timedelta
import pymysql
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()
from pathlib import Path
import os
from dotenv import load_dotenv
from decouple import config
load_dotenv()
import ssl
import certifi



BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SECRET_KEY = config('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # tu React en desarrollo
]
CORS_ALLOW_CREDENTIALS = True

# La sesión expira al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800  # sesión expira en 30 minutos de inactividad
SESSION_SAVE_EVERY_REQUEST = True  # guarda la sesión en cada solicitud

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'rest_framework',
    'usuarios',
    'restaurantes',
    'repartidores',
    'pedidos',
    'tailwind',
    'theme',
    'django_browser_reload',
    'chatbot',
    'channels',
    'django.contrib.sites',        # para entrar con google
    'allauth',                     # para entrar con google
    'allauth.account',             # para entrar con google
    'allauth.socialaccount',       # para entrar con google
    'allauth.socialaccount.providers.google',  # para entrar con google
    'contacto',  # para el formulario de contacto
]
SITE_ID = 2
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_ADAPTER = 'gastromovil.adapters.CustomSocialAccountAdapter'
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = 'index'
SOCIALACCOUNT_EMAIL_REQUIRED = False
UNIQUE_EMAIL = False
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'gastromovil.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates', BASE_DIR / 'restaurantes' / 'templates'],
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

ASGI_APPLICATION = 'gastromovil.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
} 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'gastromovil',       
        'USER': 'root',
        'PASSWORD': 'rootroot',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

print("USER:", 'root')
print("PASSWORD:", 'rootroot')
print("HOST:", 'localhost')

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',  # ← agrega esta línea
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True



STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static'),
                    os.path.join(BASE_DIR, 'theme/static'), ]

AUTH_USER_MODEL = 'usuarios.Usuario'
AUTHENTICATION_BACKENDS = [
    'usuarios.backends.EmailBackend',  
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_URL = '/usuarios/login'
#LOGIN_REDIRECT_URL = '/usuarios/perfil/'
#LOGOUT_REDIRECT_URL = '/usuarios/login/'
LOGIN_REDIRECT_URL = 'index'
ACCOUNT_LOGOUT_REDIRECT_URL = 'index'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account',
    },
    }
}

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']

JAZZMIN_SETTINGS = {
    "site_title": "GastroWeb Admin",
    "site_header": "GastroWeb",
    "site_brand": "GastroWeb",
    "welcome_sign": "Bienvenido al Panel Administrativo",
    "copyright": "GastroWeb 2026",
    "search_model": ["restaurantes.Restaurante", "restaurantes.Producto"],
    "topmenu_links": [
        {"name": "Inicio", "url": "/", "new_window": False},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "restaurantes.restaurante": "fas fa-utensils",
        "restaurantes.categoria": "fas fa-list",
        "restaurantes.producto": "fas fa-hamburger",
        "pedidos.pedido": "fas fa-shopping-bag",
        "usuarios.usuario": "fas fa-user-circle",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-danger",
    "accent": "accent-danger",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-danger",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "auto",
    "button_classes": {
        "primary": "btn-danger",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

# ✅ Un solo backend SSL para todos los send_mail del proyecto
EMAIL_BACKEND = 'usuarios.backends.SSLEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Cuenta principal (registro, verificación, recuperación)
EMAIL_HOST_USER = 'johanapalacio763@gmail.com'
EMAIL_HOST_PASSWORD = 'ecptlzagzepjejar'
DEFAULT_FROM_EMAIL = 'Gastroweb <ospinacadenaoscar@gmail.com>'

# Cuenta para contactenos (solo como variable, no como backend)
CONTACTO_EMAIL = 'ospinacadenaoscar@gmail.com'
CONTACTO_EMAIL_PASSWORD = config('CONTACTO_EMAIL_PASSWORD')